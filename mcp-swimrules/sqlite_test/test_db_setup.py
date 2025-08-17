#!/usr/bin/env python3
"""
Database Setup Test Script for Swim Rules Agent

This script tests the SQLite database functionality including:
- Basic rule storage and retrieval
- Vector embeddings storage
- Database integrity and performance

Usage:
    python test_db_setup.py [--db-path PATH]
"""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Optional


class DatabaseTestSuite:
    """Test suite for validating swim rules database functionality."""

    def __init__(self, db_path: str) -> None:
        """Initialize the test suite.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.connection: Optional[sqlite3.Connection] = None

    def __enter__(self) -> "DatabaseTestSuite":
        """Enter context manager and establish database connection."""
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.execute("PRAGMA foreign_keys=ON")

        # Load sqlite-vec extension for vector operations
        try:
            self.connection.enable_load_extension(True)
            self.connection.load_extension(
                "/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/venv/lib/python3.12/site-packages/sqlite_vec/vec0"
            )
            print("   ✓ sqlite-vec extension loaded successfully")
        except sqlite3.Error as e:
            print(f"   WARNING: Could not load sqlite-vec extension: {e}")
            print("   Vector similarity searches will fall back to text matching")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager and cleanup database connection."""
        if self.connection:
            self.connection.close()

    def test_database_functionality(self) -> bool:
        """Test all database functionality and return success status.

        Returns:
            bool: True if all tests pass, False otherwise
        """
        if not self.connection:
            raise RuntimeError("Database connection not established")

        try:
            print("Testing simplified database functionality...")

            # Run all test phases (simplified from original)
            test_phases = [
                ("Cleaning up existing test data", self._cleanup_test_data),
                ("Testing core rules table", self._test_rule_insertion),
                ("Testing vector embeddings table", self._test_vector_embeddings),
                ("Testing semantic search simulation", self._test_semantic_search_simulation),
                ("Displaying database statistics", self._show_database_statistics),
                ("Cleaning up test data", self._cleanup_test_data),
                ("Verifying cleanup", self._verify_cleanup),
            ]

            for phase_name, phase_func in test_phases:
                print(
                    f"{len([p for p, _ in test_phases[:test_phases.index((phase_name, phase_func)) + 1]])}. {phase_name}..."
                )
                if not phase_func():
                    print(f"   ERROR: {phase_name} failed")
                    return False

            print("\n✓ Database test completed successfully!")
            return True

        except sqlite3.Error as e:
            print(f"✗ Database error: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False

    def _cleanup_test_data(self) -> bool:
        """Clean up any existing test data."""
        try:
            # Delete test data in proper order (updated to match simplified schema)
            cleanup_queries = [
                "DELETE FROM vec_rules WHERE rule_id = 'test_rule_1'",
                "DELETE FROM rules WHERE rule_id = 'test_rule_1'",
            ]

            for query in cleanup_queries:
                self.connection.execute(query)

            self.connection.commit()
            print("   Test data cleaned up successfully")
            return True

        except sqlite3.Error as e:
            print(f"   WARNING: Cleanup error (may be expected): {e}")
            return True  # Continue even if cleanup fails

    def _test_rule_insertion(self) -> bool:
        """Test inserting a sample rule."""
        try:
            self.connection.execute(
                """
                INSERT INTO rules (rule_id, rule_number, rule_text, category)
                VALUES ('test_rule_1', '101.1.1',
                        'Swimmers must touch the wall with both hands simultaneously in breaststroke.',
                        'Stroke Technique')
            """
            )
            self.connection.commit()

            # Verify insertion
            cursor = self.connection.execute('SELECT COUNT(*) FROM rules WHERE rule_id = "test_rule_1"')
            count = cursor.fetchone()[0]

            if count == 1:
                print("   Core rules table test passed")
                return True
            else:
                print(f"   ERROR: Expected 1 rule, found {count}")
                return False

        except sqlite3.Error as e:
            print(f"   ERROR: Rule insertion failed: {e}")
            return False

    def _test_vector_embeddings(self) -> bool:
        """Test vector embeddings table functionality."""
        try:
            # Create a mock embedding (1536-dimensional as per OpenAI standards)
            mock_embedding = bytes([i % 256 for i in range(1536 * 4)])  # 4 bytes per float

            self.connection.execute(
                """
                INSERT INTO vec_rules (rule_id, embedding, rule_text, rule_number)
                VALUES ('test_rule_1', ?, 
                        'Swimmers must touch the wall with both hands simultaneously in breaststroke.',
                        '101.1.1')
            """,
                (mock_embedding,),
            )
            self.connection.commit()

            cursor = self.connection.execute(
                'SELECT rule_id, LENGTH(embedding) FROM vec_rules WHERE rule_id = "test_rule_1"'
            )
            vec_result = cursor.fetchone()

            if vec_result and vec_result[1] == 1536 * 4:
                print(f"   Vector embeddings test passed: {vec_result[0]},  " f"embedding size: {vec_result[1]} bytes")
                return True
            else:
                print("   ERROR: Vector embedding retrieval failed")
                return False

        except sqlite3.Error as e:
            print(f"   ERROR: Vector embeddings test failed: {e}")
            return False

    def _test_semantic_search_simulation(self) -> bool:
        """Test semantic search simulation using cosine similarity."""
        try:
            # Insert a few more test rules with embeddings for search simulation
            test_rules = [
                (
                    "test_rule_2",
                    "102.2.1",
                    "Backstroke swimmers must remain on their back throughout the race.",
                    "Stroke Technique",
                ),
                (
                    "test_rule_3",
                    "103.3.1",
                    "Butterfly swimmers must move arms simultaneously and symmetrically.",
                    "Stroke Technique",
                ),
            ]

            for rule_id, rule_number, rule_text, category in test_rules:
                # Insert rule
                self.connection.execute(
                    "INSERT INTO rules (rule_id, rule_number, rule_text, category) VALUES (?, ?, ?, ?)",
                    (rule_id, rule_number, rule_text, category),
                )

                # Insert mock embedding - create more realistic float32 embeddings
                import struct

                mock_embedding = struct.pack("f" * 1536, *[(i + hash(rule_id)) / 1536.0 for i in range(1536)])
                self.connection.execute(
                    """
                    INSERT INTO vec_rules (rule_id, embedding, rule_text, rule_number)
                    VALUES (?, ?, ?, ?)
                    """,
                    (rule_id, mock_embedding, rule_text, rule_number),
                )

            self.connection.commit()

            # Test if sqlite-vec is available for vector similarity
            try:
                # Create a query embedding for "touch wall"
                query_embedding = struct.pack("f" * 1536, *[0.1 if i < 10 else 0.0 for i in range(1536)])

                # Try vector similarity search first
                cursor = self.connection.execute(
                    """
                    SELECT rule_id, rule_number, rule_text,
                           vec_distance_cosine(embedding, ?) as distance
                    FROM vec_rules 
                    ORDER BY distance
                    LIMIT 3
                    """,
                    (query_embedding,),
                )

                search_results = cursor.fetchall()
                print(f"   Vector similarity search found {len(search_results)} matches")
                for result in search_results:
                    print(
                        f"     - {result[1]}: {result[2][:50]}... (distance: {result[3] if result[3] is not None else 0:.4f})"
                    )

            except sqlite3.Error:
                # Fall back to text search if vector functions aren't available
                print("   Falling back to text-based search...")
                cursor = self.connection.execute(
                    """
                    SELECT rule_id, rule_number, rule_text 
                    FROM vec_rules 
                    WHERE rule_text LIKE '%touch%' OR rule_text LIKE '%wall%'
                    ORDER BY rule_id
                    LIMIT 5
                """
                )

                search_results = cursor.fetchall()
                print(f"   Text-based search found {len(search_results)} matches")
                for result in search_results:
                    print(f"     - {result[1]}: {result[2][:50]}...")

            if len(search_results) > 0:
                return True
            else:
                print("   ERROR: Semantic search simulation returned no results")
                return False

        except sqlite3.Error as e:
            print(f"   ERROR: Semantic search simulation failed: {e}")
            return False
        finally:
            # Clean up additional test data
            try:
                self.connection.execute("DELETE FROM vec_rules WHERE rule_id IN ('test_rule_2', 'test_rule_3')")
                self.connection.execute("DELETE FROM rules WHERE rule_id IN ('test_rule_2', 'test_rule_3')")
                self.connection.commit()
            except sqlite3.Error:
                pass  # Ignore cleanup errors

    def _show_database_statistics(self) -> bool:
        """Display current database statistics."""
        try:
            print("\n   Database Statistics:")
            tables = ["rules", "vec_rules"]

            for table in tables:
                try:
                    cursor = self.connection.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   {table}: {count} records")
                except sqlite3.Error:
                    print(f"   {table}: Table not accessible")

            return True

        except Exception as e:
            print(f"   WARNING: Could not generate statistics: {e}")
            return True  # Non-critical failure

    def _verify_cleanup(self) -> bool:
        """Verify that test data was properly cleaned up."""
        try:
            test_tables = ["rules", "vec_rules"]

            print("\n   Post-cleanup verification:")
            cleanup_success = True

            for table in test_tables:
                cursor = self.connection.execute(f'SELECT COUNT(*) FROM {table} WHERE rule_id = "test_rule_1"')
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"   WARNING: {table} still contains {count} test records")
                    cleanup_success = False
                else:
                    print(f"   ✓ {table} cleaned successfully")

            return cleanup_success

        except sqlite3.Error as e:
            print(f"   ERROR: Cleanup verification failed: {e}")
            return False


def verify_database_exists(db_path: str) -> bool:
    """Verify that the database file exists and is accessible.

    Args:
        db_path: Path to the SQLite database file

    Returns:
        bool: True if database exists and is accessible, False otherwise
    """
    db_file = Path(db_path)
    if not db_file.exists():
        print(f"✗ Database file does not exist: {db_path}")
        print('   Run "python create_db.py" to create the database first.')
        return False

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            # Expected core tables from simplified PRD requirements (vector embeddings focus)
            expected_tables = {"rules", "vec_rules"}

            existing_tables = {table[0] for table in tables}
            missing_tables = expected_tables - existing_tables

            if missing_tables:
                print(f"✗ Database is missing required tables: {missing_tables}")
                return False

            print(f"✓ Database found with {len(existing_tables)} tables")
            return True

    except sqlite3.Error as e:
        print(f"✗ Database access error: {e}")
        return False


def main() -> None:
    """Main function to handle command line arguments and run tests."""
    # Default to the database file located alongside this script
    default_db = Path(__file__).parent / "swim_rules.db"

    parser = argparse.ArgumentParser(description="Test SQLite database functionality for Swim Rules Agent")
    parser.add_argument(
        "--db-path", default=str(default_db), help=f"Path to the SQLite database file (default: {default_db})"
    )
    parser.add_argument("--skip-verification", action="store_true", help="Skip database existence verification")

    args = parser.parse_args()

    print("=" * 60)
    print("Swim Rules Agent - Database Test Suite (Simplified)")
    print("=" * 60)

    # Verify database exists unless skipped
    if not args.skip_verification:
        if not verify_database_exists(args.db_path):
            sys.exit(1)

    # Run the functionality tests using context manager
    try:
        with DatabaseTestSuite(args.db_path) as test_suite:
            success = test_suite.test_database_functionality()

        if success:
            print("\n" + "=" * 60)
            print("✓ ALL TESTS PASSED - Database is ready for use!")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n" + "=" * 60)
            print("✗ TESTS FAILED - Database issues detected!")
            print("=" * 60)
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Test suite error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
