#!/usr/bin/env python3
"""
Database Setup Test Script for Swim Rules Agent

This script tests the SQLite database functionality including:
- Table creation and relationships
- Full-text search triggers
- Vector embeddings storage
- Rule history tracking
- Data cleanup procedures

Usage:
    python test_db_setup.py [--db-path PATH]
"""

import argparse
import sqlite3
import sys
from pathlib import Path


def test_database_functionality(db_path: str = "swim_rules.db") -> bool:
    """Test all database functionality and return success status.

    Args:
        db_path: Path to the SQLite database file

    Returns:
        bool: True if all tests pass, False otherwise
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)

        print("Testing database functionality...")

        # Clean up any existing test data first
        print("0. Cleaning up any existing test data...")
        try:
            conn.execute("DELETE FROM rule_relationships WHERE rule_id = 'test_rule_1'")
            conn.execute("DELETE FROM violations WHERE rule_id = 'test_rule_1'")
            conn.execute("DELETE FROM rule_history WHERE rule_id = 'test_rule_1'")
            conn.execute("DELETE FROM scenarios WHERE scenario_id = 'scenario_1'")
            conn.execute("DELETE FROM vec_rules WHERE rule_id = 'test_rule_1'")
            conn.execute("DELETE FROM rules WHERE rule_id = 'test_rule_1'")
            conn.commit()
            print("   Existing test data cleaned up")
        except Exception:
            print("   No existing test data found")

        # Test inserting a sample rule
        print("1. Inserting sample rule...")
        conn.execute(
            """
            INSERT INTO rules (rule_id, rule_number, rule_text, category, rule_title, section)
            VALUES ('test_rule_1', '101.1.1',
                    'Swimmers must touch the wall with both hands simultaneously in breaststroke.',
                    'Stroke Technique', 'Breaststroke Touch Requirements', '101')
        """
        )

        # Test that the FTS trigger worked
        print("2. Testing FTS trigger...")
        cursor = conn.execute('SELECT COUNT(*) FROM rules_fts WHERE rule_id = "test_rule_1"')
        fts_count = cursor.fetchone()[0]
        print(f"   FTS record created: {fts_count == 1}")
        if fts_count != 1:
            print("   ERROR: FTS trigger failed")
            return False

        # Test full-text search
        print("3. Testing full-text search...")
        cursor = conn.execute('SELECT rule_id, rule_number FROM rules_fts WHERE rules_fts MATCH "breaststroke"')
        search_results = cursor.fetchall()
        print(f"   FTS search results: {len(search_results)} matches found")
        if len(search_results) == 0:
            print("   ERROR: Full-text search failed")
            return False

        # Test updating the rule to trigger history
        print("4. Testing rule update and history trigger...")
        conn.execute(
            """
            UPDATE rules
            SET rule_text = 'Swimmers must touch the wall with both hands simultaneously in breaststroke and butterfly.'
            WHERE rule_id = 'test_rule_1'
        """
        )

        # Check that history was created
        cursor = conn.execute('SELECT COUNT(*) FROM rule_history WHERE rule_id = "test_rule_1"')
        history_count = cursor.fetchone()[0]
        print(f"   History record created: {history_count == 1}")
        if history_count != 1:
            print("   ERROR: History trigger failed")
            return False

        # Test adding related violations
        print("5. Testing violations table...")
        conn.execute(
            """
            INSERT INTO violations (violation_id, rule_id, violation_type, severity, penalty_description)
            VALUES ('viol_1', 'test_rule_1', 'STROKE_TECHNIQUE', 'DISQUALIFICATION',
                    'Immediate disqualification for improper touch')
        """
        )

        cursor = conn.execute('SELECT COUNT(*) FROM violations WHERE rule_id = "test_rule_1"')
        violation_count = cursor.fetchone()[0]
        print(f"   Violation record created: {violation_count == 1}")
        if violation_count != 1:
            print("   ERROR: Violation insertion failed")
            return False

        # Test rule relationships
        print("6. Testing rule relationships...")
        conn.execute(
            """
            INSERT INTO rule_relationships (rule_id, related_rule_id, relationship_type, strength)
            VALUES ('test_rule_1', 'test_rule_2', 'SIMILAR', 0.8)
        """
        )

        cursor = conn.execute('SELECT COUNT(*) FROM rule_relationships WHERE rule_id = "test_rule_1"')
        relationship_count = cursor.fetchone()[0]
        print(f"   Relationship record created: {relationship_count == 1}")
        if relationship_count != 1:
            print("   ERROR: Relationship insertion failed")
            return False

        # Test scenarios table
        print("7. Testing scenarios table...")
        conn.execute(
            """
            INSERT INTO scenarios (scenario_id, scenario_text, analysis_result, confidence_score)
            VALUES ('scenario_1', 'Swimmer touches wall with one hand in breaststroke',
                    '{"violation": true, "rule": "101.1.1"}', 0.95)
        """
        )

        cursor = conn.execute("SELECT COUNT(*) FROM scenarios")
        scenario_count = cursor.fetchone()[0]
        print(f"   Scenario record created: {scenario_count == 1}")
        if scenario_count != 1:
            print("   ERROR: Scenario insertion failed")
            return False

        # Test vector embeddings table
        print("8. Testing vector embeddings table...")
        # Create a mock embedding (normally this would be generated by an AI model)
        # Create a simple byte array to simulate an embedding
        mock_embedding = bytes([i % 256 for i in range(1536)])  # Mock 1536-dimensional embedding as bytes
        conn.execute(
            """
            INSERT INTO vec_rules (rule_id, embedding, dimension)
            VALUES ('test_rule_1', ?, 1536)
        """,
            (mock_embedding,),
        )

        cursor = conn.execute('SELECT COUNT(*) FROM vec_rules WHERE rule_id = "test_rule_1"')
        vec_count = cursor.fetchone()[0]
        print(f"   Vector embedding record created: {vec_count == 1}")
        if vec_count != 1:
            print("   ERROR: Vector embedding insertion failed")
            return False

        # Test retrieving the embedding
        cursor = conn.execute('SELECT rule_id, dimension FROM vec_rules WHERE rule_id = "test_rule_1"')
        vec_result = cursor.fetchone()
        if vec_result:
            print(f"   Retrieved embedding for rule: {vec_result[0]}, dimension: {vec_result[1]}")
        else:
            print("   ERROR: Could not retrieve embedding")
            return False

        # Show database statistics
        print("\n9. Database Statistics:")
        tables = ["rules", "rules_fts", "vec_rules", "violations", "rule_relationships", "rule_history", "scenarios"]
        for table in tables:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} records")

        # Clean up test data
        print("\n10. Cleaning up test data...")
        print("   Deleting test records...")

        # Delete test data in proper order (respecting foreign key constraints)
        conn.execute('DELETE FROM rule_relationships WHERE rule_id = "test_rule_1"')
        conn.execute('DELETE FROM violations WHERE rule_id = "test_rule_1"')
        conn.execute('DELETE FROM rule_history WHERE rule_id = "test_rule_1"')
        conn.execute('DELETE FROM scenarios WHERE scenario_id = "scenario_1"')
        conn.execute('DELETE FROM vec_rules WHERE rule_id = "test_rule_1"')
        # Delete from rules table last (FTS will be cleaned by trigger)
        conn.execute('DELETE FROM rules WHERE rule_id = "test_rule_1"')

        # Verify cleanup
        print("\n11. Post-cleanup Database Statistics:")
        for table in tables:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"    {table}: {count} records")
            if count != 0:
                print(f"   WARNING: {table} was not completely cleaned up")

        conn.commit()
        conn.close()
        print("\n✓ Database test completed successfully and cleaned up!")
        return True

    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
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
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()

        if len(tables) < 5:  # We expect at least 5 main tables
            print(f"✗ Database appears incomplete. Found only {len(tables)} tables.")
            return False

        print(f"✓ Database found with {len(tables)} tables")
        return True

    except sqlite3.Error as e:
        print(f"✗ Database access error: {e}")
        return False


def main():
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
    print("Swim Rules Agent - Database Test Suite")
    print("=" * 60)

    # Verify database exists unless skipped
    if not args.skip_verification:
        if not verify_database_exists(args.db_path):
            sys.exit(1)

    # Run the functionality tests
    success = test_database_functionality(args.db_path)

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


if __name__ == "__main__":
    main()
