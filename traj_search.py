#!/usr/bin/env python3
"""
Trajectory Search Utility
Helps search and analyze .traj files for coding agent trajectory annotation.
"""

import json
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import Counter


class TrajSearcher:
    """Search and analyze trajectory JSON files."""

    def __init__(self, traj_file: Path):
        """Load a trajectory file."""
        self.traj_file = traj_file
        with open(traj_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.trajectory = self.data.get('trajectory', [])

    def search_pattern(self, pattern: str, field: Optional[str] = None,
                      ignore_case: bool = True, context_lines: int = 0) -> List[Dict[str, Any]]:
        """
        Search for a regex pattern in trajectory.

        Args:
            pattern: Regex pattern to search for
            field: Specific field to search in (action, observation, thought, etc.)
                   If None, searches all text fields
            ignore_case: Whether to ignore case
            context_lines: Number of context steps to include before/after match

        Returns:
            List of matching entries with step number and matched text
        """
        flags = re.IGNORECASE if ignore_case else 0
        regex = re.compile(pattern, flags)

        results = []
        for i, step in enumerate(self.trajectory):
            # Determine which fields to search
            if field:
                fields_to_search = {field: step.get(field, '')}
            else:
                # Search common text fields
                fields_to_search = {
                    'action': step.get('action', ''),
                    'observation': step.get('observation', ''),
                    'thought': step.get('thought', ''),
                    'response': step.get('response', ''),
                }

            # Search each field
            for field_name, field_value in fields_to_search.items():
                if isinstance(field_value, str) and regex.search(field_value):
                    match_info = {
                        'step': i,
                        'field': field_name,
                        'match': field_value,
                        'step_data': step
                    }

                    # Add context if requested
                    if context_lines > 0:
                        start = max(0, i - context_lines)
                        end = min(len(self.trajectory), i + context_lines + 1)
                        match_info['context'] = self.trajectory[start:end]

                    results.append(match_info)
                    break  # Only match once per step

        return results

    def get_actions_summary(self) -> Dict[str, int]:
        """Get summary of all action types used."""
        actions = []
        for step in self.trajectory:
            action = step.get('action', '')
            if action:
                # Extract the command/tool name (first word)
                cmd = action.split()[0] if action else 'unknown'
                actions.append(cmd)

        return dict(Counter(actions))

    def get_files_viewed(self) -> List[str]:
        """Extract all files that were viewed/read."""
        files = []
        view_patterns = [
            r'view\s+([^\s]+)',
            r'cat\s+([^\s]+)',
            r'str_replace_editor\s+view\s+([^\s]+)',
            r'Read.*?file_path["\']:\s*["\']([^"\']+)',
        ]

        for step in self.trajectory:
            action = step.get('action', '')
            for pattern in view_patterns:
                matches = re.findall(pattern, action, re.IGNORECASE)
                files.extend(matches)

        return list(set(files))  # Remove duplicates

    def get_files_edited(self) -> List[str]:
        """Extract all files that were edited."""
        files = []
        edit_patterns = [
            r'str_replace_editor\s+(?:str_replace|insert|create)\s+([^\s]+)',
            r'Edit.*?file_path["\']:\s*["\']([^"\']+)',
            r'Write.*?file_path["\']:\s*["\']([^"\']+)',
        ]

        for step in self.trajectory:
            action = step.get('action', '')
            for pattern in edit_patterns:
                matches = re.findall(pattern, action, re.IGNORECASE)
                files.extend(matches)

        return list(set(files))  # Remove duplicates

    def get_tests_run(self) -> List[str]:
        """Extract test commands that were run."""
        tests = []
        test_patterns = [
            r'pytest\s+([^\s&|;]+)',
            r'python\s+-m\s+pytest\s+([^\s&|;]+)',
            r'bash.*?pytest\s+([^\s&|;]+)',
        ]

        for step in self.trajectory:
            action = step.get('action', '')
            for pattern in test_patterns:
                matches = re.findall(pattern, action, re.IGNORECASE)
                tests.extend(matches)

        return tests

    def count_occurrences(self, pattern: str, field: Optional[str] = None,
                          ignore_case: bool = True) -> int:
        """Count how many times a pattern appears."""
        return len(self.search_pattern(pattern, field, ignore_case))

    def find_step_range(self, start_pattern: str, end_pattern: str) -> List[tuple]:
        """Find ranges of steps between start and end patterns."""
        ranges = []
        in_range = False
        start_step = None

        for i, step in enumerate(self.trajectory):
            step_text = json.dumps(step)

            if re.search(start_pattern, step_text, re.IGNORECASE):
                if not in_range:
                    in_range = True
                    start_step = i

            if in_range and re.search(end_pattern, step_text, re.IGNORECASE):
                ranges.append((start_step, i))
                in_range = False
                start_step = None

        # Handle unclosed range
        if in_range and start_step is not None:
            ranges.append((start_step, len(self.trajectory) - 1))

        return ranges

    def extract_thoughts(self) -> List[Dict[str, Any]]:
        """Extract all agent thoughts/reasoning."""
        thoughts = []
        for i, step in enumerate(self.trajectory):
            thought = step.get('thought', '').strip()
            if thought:
                thoughts.append({
                    'step': i,
                    'thought': thought,
                    'action': step.get('action', '')
                })
        return thoughts

    def get_stats(self) -> Dict[str, Any]:
        """Get overall trajectory statistics."""
        return {
            'total_steps': len(self.trajectory),
            'actions_summary': self.get_actions_summary(),
            'files_viewed': len(self.get_files_viewed()),
            'files_edited': len(self.get_files_edited()),
            'tests_run': len(self.get_tests_run()),
            'has_thoughts': sum(1 for s in self.trajectory if s.get('thought', '').strip()),
        }

    def get_step(self, step_num: int) -> Optional[Dict[str, Any]]:
        """Get a single step by number."""
        if 0 <= step_num < len(self.trajectory):
            return self.trajectory[step_num]
        return None

    def parse_step_spec(self, spec: str) -> List[int]:
        """
        Parse step specification into list of step numbers.

        Supports:
        - Single step: "5"
        - Range: "5-10" (inclusive)
        - Multiple: "5,10,15"
        - Mixed: "5,10-15,20"

        Returns:
            List of step numbers (sorted, unique)
        """
        steps = set()

        # Split by comma for multiple specs
        parts = spec.split(',')

        for part in parts:
            part = part.strip()
            if '-' in part:
                # Range specification
                try:
                    start, end = part.split('-', 1)
                    start_num = int(start.strip())
                    end_num = int(end.strip())
                    steps.update(range(start_num, end_num + 1))
                except ValueError:
                    print(f"Warning: Invalid range specification: {part}")
            else:
                # Single step
                try:
                    steps.add(int(part))
                except ValueError:
                    print(f"Warning: Invalid step number: {part}")

        # Filter to valid step numbers
        valid_steps = [s for s in sorted(steps) if 0 <= s < len(self.trajectory)]
        return valid_steps

    def format_step(self, step: Dict[str, Any], step_num: int, max_len: int = 500) -> str:
        """
        Format a step for display (human-readable).

        Args:
            step: Step data
            step_num: Step number
            max_len: Maximum length for truncating long fields

        Returns:
            Formatted string representation
        """
        lines = [f"=== Step {step_num} ==="]

        # Action
        action = step.get('action', '')
        if action:
            if len(action) > max_len:
                action = action[:max_len] + '...'
            lines.append(f"Action: {action}")

        # Observation
        observation = step.get('observation', '')
        if observation:
            if len(observation) > max_len:
                observation = observation[:max_len] + '...'
            lines.append(f"Observation: {observation}")

        # Thought
        thought = step.get('thought', '').strip()
        if thought:
            if len(thought) > max_len:
                thought = thought[:max_len] + '...'
            lines.append(f"Thought: {thought}")

        # Response
        response = step.get('response', '').strip()
        if response:
            if len(response) > max_len:
                response = response[:max_len] + '...'
            lines.append(f"Response: {response}")

        # Execution time
        exec_time = step.get('execution_time')
        if exec_time is not None:
            lines.append(f"Execution time: {exec_time:.3f}s")

        return '\n'.join(lines)

    def print_steps(self, step_nums: List[int], raw: bool = False) -> None:
        """
        Print specified steps.

        Args:
            step_nums: List of step numbers to print
            raw: If True, print raw JSON; otherwise formatted
        """
        if not step_nums:
            print("No valid steps to display")
            return

        for i, step_num in enumerate(step_nums):
            step = self.get_step(step_num)
            if step is None:
                print(f"Step {step_num} not found (valid range: 0-{len(self.trajectory)-1})")
                continue

            if raw:
                print(f"=== Step {step_num} (Raw JSON) ===")
                print(json.dumps(step, indent=2))
            else:
                print(self.format_step(step, step_num))

            # Add separator between steps (except for last one)
            if i < len(step_nums) - 1:
                print()

    def get_file_modifications_evidence(self) -> Dict[str, List[int]]:
        """
        Get detailed evidence of file modifications.

        Returns:
            Dict mapping file paths to list of step numbers where they were modified
        """
        evidence = {}
        edit_patterns = [
            r'str_replace_editor\s+(?:str_replace|insert|create)\s+([^\s]+)',
            r'Edit.*?file_path["\']:\s*["\']([^"\']+)',
            r'Write.*?file_path["\']:\s*["\']([^"\']+)',
        ]

        for i, step in enumerate(self.trajectory):
            action = step.get('action', '')
            for pattern in edit_patterns:
                matches = re.findall(pattern, action, re.IGNORECASE)
                for file_path in matches:
                    if file_path not in evidence:
                        evidence[file_path] = []
                    evidence[file_path].append(i)

        return evidence

    def get_file_views_evidence(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get detailed evidence of file views including line numbers.

        Returns:
            Dict mapping file paths to list of view events with step and line info
        """
        evidence = {}

        for i, step in enumerate(self.trajectory):
            action = step.get('action', '')

            # Try to extract file path and line numbers
            # Pattern for: view /path/to/file.py 100-200
            view_with_lines = re.search(r'view\s+([^\s]+)\s+(\d+)-(\d+)', action, re.IGNORECASE)
            if view_with_lines:
                file_path = view_with_lines.group(1)
                start_line = int(view_with_lines.group(2))
                end_line = int(view_with_lines.group(3))

                if file_path not in evidence:
                    evidence[file_path] = []
                evidence[file_path].append({
                    'step': i,
                    'start_line': start_line,
                    'end_line': end_line
                })
                continue

            # Pattern for Read with offset/limit
            read_pattern = re.search(r'Read.*?file_path["\']:\s*["\']([^"\']+)["\'].*?offset["\']:\s*(\d+).*?limit["\']:\s*(\d+)', action, re.IGNORECASE)
            if read_pattern:
                file_path = read_pattern.group(1)
                offset = int(read_pattern.group(2))
                limit = int(read_pattern.group(3))

                if file_path not in evidence:
                    evidence[file_path] = []
                evidence[file_path].append({
                    'step': i,
                    'start_line': offset,
                    'end_line': offset + limit
                })
                continue

            # Simple view without line numbers
            view_patterns = [
                r'view\s+([^\s]+)',
                r'cat\s+([^\s]+)',
                r'str_replace_editor\s+view\s+([^\s]+)',
                r'Read.*?file_path["\']:\s*["\']([^"\']+)',
            ]

            for pattern in view_patterns:
                matches = re.findall(pattern, action, re.IGNORECASE)
                for file_path in matches:
                    if file_path not in evidence:
                        evidence[file_path] = []
                    evidence[file_path].append({
                        'step': i,
                        'start_line': None,
                        'end_line': None
                    })

        return evidence

    def get_search_evidence(self, pattern: str, ignore_case: bool = True) -> List[Dict[str, Any]]:
        """
        Get detailed evidence of search pattern occurrences.

        Args:
            pattern: Search pattern
            ignore_case: Whether to ignore case

        Returns:
            List of dicts with step number and context for each match
        """
        results = self.search_pattern(pattern, field=None, ignore_case=ignore_case)

        evidence = []
        for result in results:
            evidence.append({
                'step': result['step'],
                'field': result['field'],
                'context': result['match'][:200]  # First 200 chars of context
            })

        return evidence

    def get_test_evidence(self) -> List[Dict[str, Any]]:
        """
        Get detailed evidence of test runs including results.

        Returns:
            List of dicts with step, test command, and result
        """
        evidence = []
        test_patterns = [
            r'pytest\s+([^\s&|;]+)',
            r'python\s+-m\s+pytest\s+([^\s&|;]+)',
            r'bash.*?pytest\s+([^\s&|;]+)',
        ]

        for i, step in enumerate(self.trajectory):
            action = step.get('action', '')
            observation = step.get('observation', '')

            # Check if this step runs a test
            test_cmd = None
            for pattern in test_patterns:
                match = re.search(pattern, action, re.IGNORECASE)
                if match:
                    test_cmd = match.group(0)
                    break

            if test_cmd:
                # Try to determine test result from observation
                result = 'UNKNOWN'
                if observation:
                    if 'passed' in observation.lower() and 'failed' not in observation.lower():
                        result = 'PASS'
                    elif 'failed' in observation.lower() or 'error' in observation.lower():
                        result = 'FAIL'

                    # Extract specific counts if available
                    passed_match = re.search(r'(\d+)\s+passed', observation, re.IGNORECASE)
                    failed_match = re.search(r'(\d+)\s+failed', observation, re.IGNORECASE)

                    passed_count = int(passed_match.group(1)) if passed_match else 0
                    failed_count = int(failed_match.group(1)) if failed_match else 0

                    evidence.append({
                        'step': i,
                        'command': test_cmd,
                        'result': result,
                        'passed': passed_count,
                        'failed': failed_count
                    })
                else:
                    evidence.append({
                        'step': i,
                        'command': test_cmd,
                        'result': result,
                        'passed': 0,
                        'failed': 0
                    })

        return evidence

    def generate_evidence(self, evidence_type: str = 'all', **kwargs) -> str:
        """
        Generate formatted evidence for annotation.

        Args:
            evidence_type: Type of evidence to generate ('all', 'files-modified',
                          'files-viewed', 'search', 'tests')
            **kwargs: Additional arguments (e.g., pattern for search)

        Returns:
            Formatted evidence string ready for copy-paste
        """
        output_lines = []

        if evidence_type in ['all', 'files-modified']:
            output_lines.append("=== Files Modified ===")
            mods = self.get_file_modifications_evidence()
            if mods:
                for file_path, steps in sorted(mods.items()):
                    steps_str = ', '.join(map(str, steps))
                    output_lines.append(f"  {file_path}")
                    output_lines.append(f"    Modified at steps: {steps_str}")
                    output_lines.append(f"    Total modifications: {len(steps)}")
            else:
                output_lines.append("  No file modifications found")
            output_lines.append("")

        if evidence_type in ['all', 'files-viewed']:
            output_lines.append("=== Files Viewed ===")
            views = self.get_file_views_evidence()
            if views:
                for file_path, view_list in sorted(views.items()):
                    output_lines.append(f"  {file_path}")
                    for view in view_list[:5]:  # Show first 5 views
                        if view['start_line'] is not None:
                            output_lines.append(f"    Step {view['step']}: lines {view['start_line']}-{view['end_line']}")
                        else:
                            output_lines.append(f"    Step {view['step']}: (full file)")
                    if len(view_list) > 5:
                        output_lines.append(f"    ... and {len(view_list)-5} more views")
                    output_lines.append(f"    Total views: {len(view_list)}")
            else:
                output_lines.append("  No file views found")
            output_lines.append("")

        if evidence_type in ['search'] or (evidence_type == 'all' and kwargs.get('pattern')):
            pattern = kwargs.get('pattern', '')
            if pattern:
                output_lines.append(f"=== Search Pattern: '{pattern}' ===")
                search_ev = self.get_search_evidence(pattern)
                if search_ev:
                    steps = [ev['step'] for ev in search_ev]
                    steps_str = ', '.join(map(str, steps[:10]))
                    if len(steps) > 10:
                        steps_str += f", ... ({len(steps)-10} more)"
                    output_lines.append(f"  Found {len(search_ev)} occurrences")
                    output_lines.append(f"  Steps: {steps_str}")
                    output_lines.append("")
                    output_lines.append("  Sample matches:")
                    for ev in search_ev[:3]:
                        output_lines.append(f"    Step {ev['step']} ({ev['field']}): {ev['context'][:100]}...")
                else:
                    output_lines.append("  No matches found")
                output_lines.append("")

        if evidence_type in ['all', 'tests']:
            output_lines.append("=== Test Execution ===")
            tests = self.get_test_evidence()
            if tests:
                output_lines.append(f"  Total test runs: {len(tests)}")
                output_lines.append("")
                for test in tests:
                    result_str = test['result']
                    if test['passed'] > 0 or test['failed'] > 0:
                        result_str += f" ({test['passed']} passed, {test['failed']} failed)"
                    output_lines.append(f"  Step {test['step']}: {result_str}")
                    output_lines.append(f"    Command: {test['command']}")
            else:
                output_lines.append("  No test runs found")
            output_lines.append("")

        return '\n'.join(output_lines)


def main():
    """CLI interface for trajectory search."""
    parser = argparse.ArgumentParser(
        description='Search and analyze coding agent trajectory files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for VAR_FLAGS mentions
  python traj_search.py trace_01.traj --search "VAR_FLAGS"

  # Count how many times agent viewed a specific file
  python traj_search.py trace_01.traj --search "nodes.py" --count

  # Get summary statistics
  python traj_search.py trace_01.traj --stats

  # Find what files were viewed
  python traj_search.py trace_01.traj --files-viewed

  # View a specific step
  python traj_search.py trace_01.traj --step 5

  # View a range of steps
  python traj_search.py trace_01.traj --steps 5-10

  # View multiple specific steps
  python traj_search.py trace_01.traj --steps 5,10,15

  # View step as raw JSON
  python traj_search.py trace_01.traj --step 5 --raw

  # Search only in actions
  python traj_search.py trace_01.traj --search "grep" --field action

  # Extract all agent thoughts
  python traj_search.py trace_01.traj --thoughts

  # Generate all evidence for annotation (QA mode)
  python traj_search.py trace_01.traj --evidence

  # Generate specific evidence type
  python traj_search.py trace_01.traj --evidence files-modified
  python traj_search.py trace_01.traj --evidence files-viewed
  python traj_search.py trace_01.traj --evidence tests

  # Generate search evidence with pattern
  python traj_search.py trace_01.traj --evidence search --evidence-pattern "VAR_FLAGS"
        """
    )

    parser.add_argument('traj_file', type=Path, help='Path to .traj file')
    parser.add_argument('--search', '-s', help='Search pattern (regex)')
    parser.add_argument('--field', '-f', choices=['action', 'observation', 'thought', 'response'],
                       help='Specific field to search in')
    parser.add_argument('--count', '-c', action='store_true',
                       help='Just count occurrences, don\'t show matches')

    # Case sensitivity - mutually exclusive group
    search_case = parser.add_mutually_exclusive_group()
    search_case.add_argument('-i', '--ignore-case', dest='ignore_case',
                            action='store_true', default=True,
                            help='Case-insensitive search (default)')
    search_case.add_argument('--case-sensitive', dest='ignore_case',
                            action='store_false',
                            help='Case-sensitive search')
    parser.add_argument('--context', type=int, default=0, metavar='N',
                       help='Show N steps of context around matches')
    parser.add_argument('--stats', action='store_true',
                       help='Show trajectory statistics')
    parser.add_argument('--files-viewed', action='store_true',
                       help='List all files that were viewed')
    parser.add_argument('--files-edited', action='store_true',
                       help='List all files that were edited')
    parser.add_argument('--tests-run', action='store_true',
                       help='List all test commands run')
    parser.add_argument('--thoughts', action='store_true',
                       help='Extract all agent thoughts/reasoning')
    parser.add_argument('--step', type=str, metavar='SPEC',
                       help='Show specific step(s): single (5), range (5-10), or multiple (5,10,15)')
    parser.add_argument('--steps', type=str, metavar='SPEC',
                       help='Alias for --step')
    parser.add_argument('--raw', action='store_true',
                       help='Show raw JSON for steps (use with --step/--steps)')
    parser.add_argument('--max-results', '-m', type=int, default=None,
                       help='Maximum number of results to show')
    parser.add_argument('--evidence', type=str, nargs='?', const='all',
                       choices=['all', 'files-modified', 'files-viewed', 'search', 'tests'],
                       help='Generate evidence for annotation (all, files-modified, files-viewed, search, tests)')
    parser.add_argument('--evidence-pattern', type=str,
                       help='Search pattern for evidence mode (use with --evidence search)')

    # Parse args with custom error handling
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # Check if user tried common grep flags
        if e.code == 2:  # Parse error
            if '-i' in sys.argv:
                print("\n💡 Note: This tool is case-insensitive by default.", file=sys.stderr)
                print("   The -i flag is not needed (it's already the default behavior).", file=sys.stderr)
                print("   Use --case-sensitive if you want case-sensitive search.\n", file=sys.stderr)
        raise

    if not args.traj_file.exists():
        print(f"Error: File not found: {args.traj_file}")
        return 1

    searcher = TrajSearcher(args.traj_file)

    # Handle different modes
    if args.evidence:
        # Evidence generation mode
        kwargs = {}
        if args.evidence_pattern:
            kwargs['pattern'] = args.evidence_pattern
        elif args.evidence == 'search' and args.search:
            kwargs['pattern'] = args.search

        evidence_output = searcher.generate_evidence(args.evidence, **kwargs)
        print(evidence_output)

    elif args.stats:
        stats = searcher.get_stats()
        print(f"=== Trajectory Statistics ===")
        print(f"Total steps: {stats['total_steps']}")
        print(f"Files viewed: {stats['files_viewed']}")
        print(f"Files edited: {stats['files_edited']}")
        print(f"Tests run: {stats['tests_run']}")
        print(f"Steps with thoughts: {stats['has_thoughts']}")
        print(f"\n=== Action Summary ===")
        for action, count in sorted(stats['actions_summary'].items(), key=lambda x: -x[1]):
            print(f"  {action}: {count}")

    elif args.files_viewed:
        files = searcher.get_files_viewed()
        print(f"=== Files Viewed ({len(files)}) ===")
        for f in sorted(files):
            print(f"  {f}")

    elif args.files_edited:
        files = searcher.get_files_edited()
        print(f"=== Files Edited ({len(files)}) ===")
        for f in sorted(files):
            print(f"  {f}")

    elif args.tests_run:
        tests = searcher.get_tests_run()
        print(f"=== Tests Run ({len(tests)}) ===")
        for t in tests:
            print(f"  {t}")

    elif args.thoughts:
        thoughts = searcher.extract_thoughts()
        print(f"=== Agent Thoughts ({len(thoughts)}) ===\n")
        for t in thoughts[:args.max_results] if args.max_results else thoughts:
            print(f"Step {t['step']}:")
            print(f"  Action: {t['action'][:80]}...")
            print(f"  Thought: {t['thought'][:200]}...")
            print()

    elif args.step or args.steps:
        # Use --steps if provided, otherwise --step
        step_spec = args.steps if args.steps else args.step
        step_nums = searcher.parse_step_spec(step_spec)

        if not step_nums:
            print(f"No valid steps found in specification: {step_spec}")
            print(f"Valid range: 0-{len(searcher.trajectory)-1}")
        else:
            searcher.print_steps(step_nums, raw=args.raw)

    elif args.search:
        results = searcher.search_pattern(
            args.search,
            field=args.field,
            ignore_case=args.ignore_case,
            context_lines=args.context
        )

        if args.count:
            print(f"Found {len(results)} occurrences of '{args.search}'")
        else:
            print(f"=== Search Results for '{args.search}' ({len(results)} matches) ===\n")
            for i, result in enumerate(results[:args.max_results] if args.max_results else results):
                print(f"Match {i+1} - Step {result['step']} - Field: {result['field']}")
                match_text = result['match']
                # Highlight the match
                highlighted = re.sub(
                    f"({args.search})",
                    r">>> \1 <<<",
                    match_text[:500],
                    flags=re.IGNORECASE if args.ignore_case else 0
                )
                print(f"  {highlighted}")
                print()

    else:
        parser.print_help()

    return 0


if __name__ == '__main__':
    exit(main())
