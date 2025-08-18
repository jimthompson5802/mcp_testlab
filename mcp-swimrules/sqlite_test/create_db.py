#!/usr/bin/env python3
"""
Database Creation Script for Swim Rules Agent

This script creates the SQLite database schema for the USA Swimming rules
application with support for vector embeddings and semantic search.

Usage:
    python create_db.py [--db-path PATH] [--force]

Arguments:
    --db-path: Path where to create the database (default: swim_rules.db)
    --force: Overwrite existing database if it exists
"""

import argparse
import sqlite3
import sys
from pathlib import Path


class SwimRulesDatabaseCreator:
    """Creates and initializes the swim rules SQLite database."""

    def __init__(self, db_path: str) -> None:
        """Initialize the database creator.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)

    def create_database(self, force: bool = False) -> None:
        """Create the database and all required tables.

        Args:
            force: If True, overwrite existing database

        Raises:
            FileExistsError: If database exists and force is False
            sqlite3.Error: If database creation fails
        """
        if self.db_path.exists() and not force:
            raise FileExistsError(f"Database already exists at {self.db_path}. Use --force to overwrite.")

        if self.db_path.exists() and force:
            print(f"Removing existing database: {self.db_path}")
            self.db_path.unlink()

        print(f"Creating database: {self.db_path}")

        try:
            self.connection = sqlite3.connect(str(self.db_path))
            vec_extension_loaded = self._enable_extensions()
            self._create_tables(vec_extension_loaded)
            self._create_indices()
            self._configure_database()
            self.connection.commit()
            print("Database created successfully!")

        except sqlite3.Error as e:
            print(f"Error creating database: {e}")
            if self.db_path.exists():
                self.db_path.unlink()
            raise
        finally:
            if hasattr(self, "connection") and self.connection:
                self.connection.close()

    def _enable_extensions(self) -> bool:
        """Enable SQLite extensions for vector operations.

        Returns:
            bool: True if sqlite-vec extension loaded, False otherwise
        """
        try:
            self.connection.enable_load_extension(True)
            possible_names = [
                "sqlite_vec",
                "sqlite-vec",
                "vec",
                "vec0",
                "/Users/jim/Desktop/modelcontextprotocol/mcp_testlab/venv/lib/python3.12/site-packages/sqlite_vec/vec0",
            ]
            loaded = False
            for name in possible_names:
                print(f"Attempting to load sqlite-vec extension: {name}")
                try:
                    self.connection.execute(f"SELECT load_extension('{name}')")
                    print(f"✓ Loaded sqlite-vec extension: {name}")
                    loaded = True
                    break
                except sqlite3.OperationalError:
                    print(f"failed to load {name}")
                    continue

            if not loaded:
                print("⚠️ Could not load sqlite-vec extension. Proceeding without vector extension.")
            self.connection.enable_load_extension(False)
            return loaded
        except Exception as e:
            print(f"⚠️ Error loading sqlite-vec extension: {e}. Proceeding without vector extension.")
            return False

    def _create_tables(self, vec_extension_loaded: bool = False) -> None:
        """Create all required database tables.

        Args:
            vec_extension_loaded: Whether the sqlite-vec extension was loaded
        """

        # Core rules table (extended for PRD compliance)
        self.connection.execute(
            """
            CREATE TABLE rules (
                rule_id TEXT PRIMARY KEY,
                rule_number TEXT NOT NULL,
                rule_text TEXT NOT NULL,
                category TEXT NOT NULL,
                section TEXT,
                subsection TEXT,
                source TEXT,
                version INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(rule_number, version)
            )
        """
        )
        print("✓ Created rules table")

        # Vector embeddings table using sqlite-vec (primary focus from PRD)
        if vec_extension_loaded:
            self.connection.execute(
                """
                CREATE VIRTUAL TABLE vec_rules USING vec0(
                    embedding float[1536],
                    rule_id TEXT PRIMARY KEY,
                    rule_text TEXT,
                    rule_number TEXT
                )
            """
            )
            print("✓ Created vec_rules vector embeddings table (virtual table for sqlite-vec)")
        else:
            print("Skipped creating vec_rules virtual table (sqlite-vec extension not loaded)")

        # Fallback vector embeddings table for development without sqlite-vec
        self.connection.execute(
            """
            CREATE TABLE vec_rules_fallback (
                rule_id TEXT PRIMARY KEY,
                embedding BLOB,
                rule_text TEXT,
                rule_number TEXT,
                source TEXT,
                dimension INTEGER DEFAULT 1536,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created vec_rules_fallback table for development")

    def _create_indices(self) -> None:
        """Create database indices for optimal query performance."""

        # Performance indexes for rules table
        self.connection.execute("CREATE INDEX idx_rules_category ON rules(category)")
        self.connection.execute("CREATE INDEX idx_rules_version ON rules(version)")
        self.connection.execute("CREATE INDEX idx_rules_number ON rules(rule_number)")
        print("✓ Created rules table indices")

        # Index for fallback vector table
        self.connection.execute("CREATE INDEX idx_vec_fallback_rule_id ON vec_rules_fallback(rule_id)")
        print("✓ Created vector embeddings indices")

    def _configure_database(self) -> None:
        """Configure SQLite database settings for optimal performance."""

        # Enable WAL mode for better concurrency
        self.connection.execute("PRAGMA journal_mode=WAL")

        # Set synchronous mode for balance between safety and performance
        self.connection.execute("PRAGMA synchronous=NORMAL")

        # Increase cache size for better performance
        self.connection.execute("PRAGMA cache_size=10000")

        # Enable foreign key constraints
        self.connection.execute("PRAGMA foreign_keys=ON")

        print("✓ Configured database settings")

    def verify_database(self) -> bool:
        """Verify that all tables and indices were created successfully.

        Returns:
            bool: True if verification passes, False otherwise
        """
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Check that core tables exist (simplified from PRD)
            expected_tables = ["rules", "vec_rules_fallback"]

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]

            missing_tables = set(expected_tables) - set(existing_tables)
            if missing_tables:
                print(f"✗ Missing tables: {missing_tables}")
                return False

            print("✓ All required tables exist")

            # Check that indices exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indices = [row[0] for row in cursor.fetchall()]

            if len(indices) < 3:  # We created 4 indices
                print(f"✗ Expected at least 3 indices, found {len(indices)}")
                return False

            print(f"✓ Found {len(indices)} indices")

            return True

        except sqlite3.Error as e:
            print(f"✗ Verification failed: {e}")
            return False
        finally:
            if connection:
                connection.close()


def main() -> None:
    """Main function to handle command line arguments and create database."""
    parser = argparse.ArgumentParser(description="Create SQLite database for Swim Rules Agent")
    parser.add_argument(
        "--db-path", default="swim_rules.db", help="Path where to create the database (default: swim_rules.db)"
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing database if it exists")
    parser.add_argument("--verify", action="store_true", help="Verify database structure after creation")

    args = parser.parse_args()

    try:
        creator = SwimRulesDatabaseCreator(args.db_path)
        creator.create_database(force=args.force)

        if args.verify:
            print("\nVerifying database structure...")
            if creator.verify_database():
                print("✓ Database verification passed")
            else:
                print("✗ Database verification failed")
                sys.exit(1)

        print(f"\nDatabase successfully created at: {Path(args.db_path).absolute()}")

    except FileExistsError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
