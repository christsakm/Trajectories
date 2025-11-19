#!/usr/bin/env python3
"""
Script to count words in rubric rationale and criterion fields from evaluation.txt files.
"""
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def count_words(text: str) -> int:
    """Count words in a text string."""
    if not text:
        return 0
    # Remove extra whitespace and split by spaces
    words = text.strip().split()
    return len(words)


def extract_rubrics_from_file(file_path: Path) -> Dict:
    """Extract rubrics section from evaluation.txt file."""
    content = file_path.read_text(encoding='utf-8')

    # Find the Rubrics section
    rubrics_match = re.search(r'Rubrics \*\s*.*\n({.*?})\s*\n\s*Rubrics rating', content, re.DOTALL)

    if not rubrics_match:
        return {}

    rubrics_json = rubrics_match.group(1)

    try:
        rubrics = json.loads(rubrics_json)
        return rubrics
    except json.JSONDecodeError as e:
        print(f"Error parsing rubrics from {file_path}: {e}")
        return {}


def extract_trace_rationales_from_file(file_path: Path) -> Dict:
    """Extract trace rationales from the 'Overall rating' section of an evaluation.txt file."""
    content = file_path.read_text(encoding='utf-8')
    
    # Find the Overall rating section
    rating_match = re.search(r'Overall rating \*\s*.*\n({.*?})\s*$', content, re.DOTALL)

    if not rating_match:
        return {}

    rating_json = rating_match.group(1)

    try:
        ratings = json.loads(rating_json)
        return ratings
    except json.JSONDecodeError as e:
        print(f"Error parsing 'Overall rating' from {file_path}: {e}")
        return {}


def analyze_rubrics(rubrics: Dict, file_name: str) -> Tuple[List[Dict], Dict]:
    """Analyze rubrics and return word counts."""
    results = []
    totals = {
        'criterion_words': 0,
        'rationale_words': 0,
        'total_rubrics': 0
    }

    for rubric_id, rubric in sorted(rubrics.items()):
        if not isinstance(rubric, dict):
            continue

        criterion = rubric.get('criterion', '')
        rationale = rubric.get('rationale', '')

        criterion_count = count_words(criterion)
        rationale_count = count_words(rationale)

        results.append({
            'id': rubric_id,
            'criterion_words': criterion_count,
            'rationale_words': rationale_count,
            'total_words': criterion_count + rationale_count,
            'type': rubric.get('type', 'unknown'),
            'importance': rubric.get('importance', 'unknown')
        })

        totals['criterion_words'] += criterion_count
        totals['rationale_words'] += rationale_count
        totals['total_rubrics'] += 1

    return results, totals


def analyze_trace_rationales(ratings: Dict) -> Tuple[List[Dict], int]:
    """Analyze trace rationales and return word counts."""
    results = []
    total_words = 0
    for trace_id, details in sorted(ratings.items()):
        if isinstance(details, dict) and 'rationale' in details:
            rationale = details['rationale']
            word_count = count_words(rationale)
            results.append({'id': trace_id, 'rationale_words': word_count})
            total_words += word_count
    return results, total_words


def print_analysis(file_name: str, rubric_results: List[Dict], rubric_totals: Dict, trace_results: List[Dict], trace_total_words: int):
    """Print analysis results."""
    print(f"\n{'='*80}")
    print(f"FILE: {file_name}")
    print(f"{'='*80}")

    if rubric_results:
        print(f"\nTotal Rubrics: {rubric_totals['total_rubrics']}")
        print(f"\n{'Rubric':<12} {'Type':<15} {'Importance':<15} {'Criterion':<12} {'Rationale':<12} {'Total':<10}")
        print("-" * 80)

        for r in rubric_results:
            print(f"{r['id']:<12} {r['type']:<15} {r['importance']:<15} "
                  f"{r['criterion_words']:<12} {r['rationale_words']:<12} {r['total_words']:<10}")

        print("-" * 80)
        print(f"{'TOTALS':<42} {rubric_totals['criterion_words']:<12} {rubric_totals['rationale_words']:<12} "
              f"{rubric_totals['criterion_words'] + rubric_totals['rationale_words']:<10}")

        if rubric_totals['total_rubrics'] > 0:
            avg_criterion = rubric_totals['criterion_words'] / rubric_totals['total_rubrics']
            avg_rationale = rubric_totals['rationale_words'] / rubric_totals['total_rubrics']
            print(f"{'AVERAGES':<42} {avg_criterion:<12.1f} {avg_rationale:<12.1f} "
                  f"{(avg_criterion + avg_rationale):<10.1f}")

    if trace_results:
        print(f"\nTrace Rationale Word Counts")
        print("-" * 80)
        for r in trace_results:
            print(f"{r['id']:<12} {r['rationale_words']} words")
        print("-" * 80)
        print(f"Total Trace Rationale Words: {trace_total_words}")


def main():
    """Main function to analyze evaluation.txt files."""
    parser = argparse.ArgumentParser(description="Count words in rubric rationale and criterion fields from evaluation.txt files.")
    parser.add_argument("file_path", nargs="?", default=None, help="Optional: Path to a specific evaluation.txt file to analyze.")
    args = parser.parse_args()

    if args.file_path:
        eval_files = [Path(args.file_path)]
        if not eval_files[0].exists():
            print(f"Error: File not found: {args.file_path}")
            return
    else:
        # Get all evaluation.txt files
        trajectories_dir = Path(__file__).parent
        # Find all evaluation.txt files
        eval_files = list(trajectories_dir.rglob("evaluation.txt"))

    if not eval_files:
        print("No evaluation.txt files found!")
        return

    print(f"\nFound {len(eval_files)} evaluation.txt file(s)")

    all_totals = []

    for eval_file in sorted(eval_files):
        rubrics = extract_rubrics_from_file(eval_file)
        ratings = extract_trace_rationales_from_file(eval_file)

        if not rubrics and not ratings:
            print(f"\nWarning: No rubrics or ratings found in {eval_file}")
            continue
        
        rubric_results, rubric_totals = analyze_rubrics(rubrics, eval_file.parent.name)
        trace_results, trace_total_words = analyze_trace_rationales(ratings)
        
        print_analysis(eval_file.parent.name, rubric_results, rubric_totals, trace_results, trace_total_words)

        rubric_totals['trace_rationale_words'] = trace_total_words
        all_totals.append({
            'file': eval_file.parent.name,
            'totals': rubric_totals
        })

    # Print summary
    if len(all_totals) > 1:
        print(f"\n{'='*80}")
        print("SUMMARY ACROSS ALL FILES")
        print(f"{'='*80}\n")

        print(f"{'File':<30} {'Rubrics':<10} {'Criterion':<12} {'Rubric Rationale':<20} {'Trace Rationale':<20}")
        print("-" * 100)

        grand_totals = {'criterion_words': 0, 'rationale_words': 0, 'total_rubrics': 0, 'trace_rationale_words': 0}

        for item in all_totals:
            totals = item['totals']
            print(f"{item['file']:<30} {totals.get('total_rubrics', 0):<10} "
                  f"{totals.get('criterion_words', 0):<12} {totals.get('rationale_words', 0):<20} "
                  f"{totals.get('trace_rationale_words', 0):<20}")

            grand_totals['criterion_words'] += totals.get('criterion_words', 0)
            grand_totals['rationale_words'] += totals.get('rationale_words', 0)
            grand_totals['total_rubrics'] += totals.get('total_rubrics', 0)
            grand_totals['trace_rationale_words'] += totals.get('trace_rationale_words', 0)

        print("-" * 100)
        print(f"{'GRAND TOTALS':<30} {grand_totals['total_rubrics']:<10} "
              f"{grand_totals['criterion_words']:<12} {grand_totals['rationale_words']:<20} "
              f"{grand_totals['trace_rationale_words']:<20}")

        if grand_totals['total_rubrics'] > 0:
            avg_criterion = grand_totals['criterion_words'] / grand_totals['total_rubrics']
            avg_rationale = grand_totals['rationale_words'] / grand_totals['total_rubrics']
            # Note: Average for trace rationale might be better per trace than per rubric
            print(f"{'GRAND AVERAGES (per rubric)':<30} {'':<10} {avg_criterion:<12.1f} {avg_rationale:<20.1f}")


if __name__ == "__main__":
    main()
