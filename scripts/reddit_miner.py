#!/usr/bin/env python3
"""
Reddit content idea miner for Inito SEO.
Mines posts and top comments from target subreddits and extracts
question patterns, pain points, and topic seeds.

Usage:
    # Browse subreddits from config
    python3 reddit_miner.py --limit 75 --sort top --comments 10

    # Override subreddits at runtime
    python3 reddit_miner.py --subreddits TryingForABaby,PCOS --comments 10

    # Search by keyword phrase within subreddits
    python3 reddit_miner.py --search "ovulation PCOS" --subreddits TryingForABaby,PCOS

    # JSON output for piping
    python3 reddit_miner.py --json --limit 50
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import praw

CONFIG_PATH = Path(__file__).parent.parent / "config" / "reddit_config.json"

QUESTION_PATTERNS = re.compile(
    r"\b(how|why|when|what|does|can|is|are|should|will|which|do i|anyone|has anyone|"
    r"help|advice|confused|struggling|wondering|question)\b",
    re.IGNORECASE,
)

TOPIC_SEEDS = {
    "ovulation_tracking": [
        "ovulation", "LH surge", "LH peak", "OPK", "ovulation test", "ovulation strip",
        "positive OPK", "LH", "fertile window",
    ],
    "hormone_monitoring": [
        "hormone", "estrogen", "progesterone", "PdG", "FSH", "AMH", "LH level",
        "hormone test", "hormones", "hormone tracker",
    ],
    "fertility_monitors": [
        "fertility monitor", "inito", "mira", "clearblue", "ava bracelet",
        "kegg", "tempdrop", "wearable", "fertility device",
    ],
    "irregular_cycles": [
        "irregular cycle", "irregular period", "short cycle", "long cycle",
        "anovulatory", "no ovulation", "PCOS cycle", "luteal phase",
    ],
    "pcos": [
        "PCOS", "polycystic", "insulin resistance", "metformin", "inositol",
        "PCOS ovulation", "PCOS tracking",
    ],
    "ttc_timing": [
        "best time to conceive", "timing intercourse", "timed intercourse",
        "fertile days", "conception window", "baby dance", "BD timing",
    ],
    "confirmed_ovulation": [
        "confirm ovulation", "confirmed ovulation", "progesterone after ovulation",
        "did i ovulate", "temp shift", "BBT", "basal body temperature",
    ],
    "unexplained_infertility": [
        "unexplained infertility", "failed IUI", "failed IVF", "trying for years",
        "RE", "reproductive endocrinologist", "cycle failed",
    ],
    "early_pregnancy": [
        "implantation", "early pregnancy", "HCG", "pregnancy test", "BFP",
        "DPO", "symptoms", "early signs",
    ],
    "product_comparison": [
        "vs", "compared to", "better than", "recommend", "worth it",
        "which monitor", "best fertility", "review",
    ],
}


def connect(config: dict) -> praw.Reddit:
    return praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=config["user_agent"],
    )


def score_topic(title: str, body: str = "") -> list[str]:
    text = f"{title} {body}".lower()
    return [
        topic
        for topic, keywords in TOPIC_SEEDS.items()
        if any(kw.lower() in text for kw in keywords)
    ]


def is_question_or_pain_point(title: str) -> bool:
    return bool(QUESTION_PATTERNS.search(title)) or title.strip().endswith("?")


def fetch_top_comments(submission, top_n: int = 10) -> list[dict]:
    """Fetch the top N top-level comments by score."""
    try:
        submission.comments.replace_more(limit=0)
        top_level = [c for c in submission.comments if hasattr(c, "body")]
        top_level.sort(key=lambda c: c.score, reverse=True)
        return [
            {"body": c.body[:500], "score": c.score}
            for c in top_level[:top_n]
            if c.body not in ("[deleted]", "[removed]")
        ]
    except Exception:
        return []


def mine_subreddit(
    reddit: praw.Reddit,
    subreddit_name: str,
    limit: int,
    sort: str,
    comments_per_post: int,
    search_phrase: str | None = None,
) -> list[dict]:
    sub = reddit.subreddit(subreddit_name)
    posts = []

    if search_phrase:
        listing = sub.search(search_phrase, sort="top", time_filter="year", limit=limit)
    else:
        fetch_fn = {
            "hot": sub.hot,
            "top": lambda limit: sub.top(time_filter="year", limit=limit),
            "new": sub.new,
        }.get(sort, sub.hot)
        listing = fetch_fn(limit=limit)

    try:
        for post in listing:
            body_snippet = getattr(post, "selftext", "")[:500]
            topics = score_topic(post.title, body_snippet)
            comments = fetch_top_comments(post, comments_per_post) if comments_per_post > 0 else []

            # include comment text in topic scoring
            comment_text = " ".join(c["body"] for c in comments)
            if comment_text:
                topics = list(set(topics + score_topic("", comment_text)))

            posts.append(
                {
                    "subreddit": subreddit_name,
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "url": f"https://reddit.com{post.permalink}",
                    "flair": post.link_flair_text,
                    "is_question": is_question_or_pain_point(post.title),
                    "topics": topics,
                    "engagement": post.score + post.num_comments * 3,
                    "top_comments": comments,
                }
            )
    except Exception as e:
        print(f"  [!] Error mining r/{subreddit_name}: {e}", file=sys.stderr)

    return posts


def cluster_by_topic(posts: list[dict]) -> dict[str, list[dict]]:
    clusters: dict[str, list[dict]] = defaultdict(list)
    for post in posts:
        for topic in post["topics"]:
            clusters[topic].append(post)
        if not post["topics"]:
            clusters["_uncategorized"].append(post)
    return dict(clusters)


def top_posts_per_topic(
    clusters: dict[str, list[dict]], top_n: int = 5
) -> dict[str, list[dict]]:
    return {
        topic: sorted(posts, key=lambda p: p["engagement"], reverse=True)[:top_n]
        for topic, posts in clusters.items()
        if topic != "_uncategorized"
    }


def extract_seed_phrases(posts: list[dict]) -> list[str]:
    return [
        p["title"]
        for p in sorted(posts, key=lambda x: x["engagement"], reverse=True)
        if p["is_question"]
    ][:20]


def extract_comment_seeds(posts: list[dict]) -> list[str]:
    """Pull notable phrases from top comments across posts."""
    fragments = []
    for post in sorted(posts, key=lambda p: p["engagement"], reverse=True)[:10]:
        for comment in post.get("top_comments", [])[:3]:
            # grab sentences that contain question markers
            sentences = re.split(r"[.!?\n]", comment["body"])
            for s in sentences:
                s = s.strip()
                if s and QUESTION_PATTERNS.search(s) and 10 < len(s) < 120:
                    fragments.append(s)
    return fragments[:10]


_clusters_raw: dict = {}


def summarize(all_posts: list[dict], top_by_topic: dict) -> dict:
    by_sub: dict[str, int] = defaultdict(int)
    for p in all_posts:
        by_sub[p["subreddit"]] += 1

    topic_summary = {}
    for topic, posts in top_by_topic.items():
        topic_summary[topic] = {
            "post_count": len(_clusters_raw.get(topic, [])),
            "top_engagement": posts[0]["engagement"] if posts else 0,
            "sample_titles": [p["title"] for p in posts[:3]],
            "seed_phrases": extract_seed_phrases(posts),
            "comment_seeds": extract_comment_seeds(posts),
        }

    return {
        "total_posts_scraped": len(all_posts),
        "question_posts": sum(1 for p in all_posts if p["is_question"]),
        "posts_by_subreddit": dict(by_sub),
        "topic_clusters": topic_summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Mine Reddit for SEO content ideas")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--limit", type=int, default=75, help="Posts per subreddit")
    parser.add_argument("--sort", default="top", choices=["hot", "top", "new"])
    parser.add_argument(
        "--comments", type=int, default=10,
        help="Top comments to fetch per post (0 to skip, slower when >0)"
    )
    parser.add_argument(
        "--subreddits", type=str, default=None,
        help="Comma-separated subreddits to mine (overrides config)"
    )
    parser.add_argument(
        "--search", type=str, default=None,
        help="Search phrase to use within each subreddit instead of browsing"
    )
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text())
    reddit = connect(config)

    if args.subreddits:
        subreddits = [s.strip() for s in args.subreddits.split(",")]
    else:
        subreddits = config["target_subreddits"]

    all_posts: list[dict] = []

    if not args.json:
        mode = f'search="{args.search}"' if args.search else f"sort={args.sort}"
        print(f"Mining {len(subreddits)} subreddits ({args.limit} posts each, {mode}, comments={args.comments})...\n")

    for sub in subreddits:
        if not args.json:
            print(f"  r/{sub}...")
        posts = mine_subreddit(reddit, sub, args.limit, args.sort, args.comments, args.search)
        all_posts.extend(posts)
        if not args.json:
            q = sum(1 for p in posts if p["is_question"])
            print(f"    {len(posts)} posts, {q} questions")

    global _clusters_raw
    _clusters_raw = cluster_by_topic(all_posts)
    top_by_topic = top_posts_per_topic(_clusters_raw, top_n=5)
    summary = summarize(all_posts, top_by_topic)

    if args.json:
        print(json.dumps({"summary": summary, "top_posts_by_topic": top_by_topic}, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"TOTAL: {summary['total_posts_scraped']} posts | {summary['question_posts']} questions\n")
        for topic, data in summary["topic_clusters"].items():
            print(f"\n--- {topic.upper().replace('_', ' ')} ({data['post_count']} posts) ---")
            for title in data["sample_titles"]:
                print(f"  • {title}")
            if data["seed_phrases"]:
                print(f"  Seed titles : {data['seed_phrases'][0]}")
            if data["comment_seeds"]:
                print(f"  Comment seed: {data['comment_seeds'][0]}")


if __name__ == "__main__":
    main()
