#!/usr/bin/env python3
"""
Database Creation Script for Swim Rules Agent

This script creates the SQLite database schema for the USA Swimming rules
application with support for full-text search and vector embeddings.

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
            raise FileExistsError(f"Database already exists at {self.db_path}. " "Use --force to overwrite.")

        if self.db_path.exists() and force:
            print(f"Removing existing database: {self.db_path}")
            self.db_path.unlink()

        print(f"Creating database: {self.db_path}")

        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self._enable_extensions()
            self._create_tables()
            self._create_indices()
            self._create_triggers()
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

    def _enable_extensions(self) -> None:
        """Enable SQLite extensions for full-text search and vector operations."""
        # Enable FTS5 (usually built-in)
        self.connection.execute("SELECT fts5(?)", ("test",))
        print("✓ FTS5 extension enabled")

        # Note: sqlite-vec extension would be loaded here in production
        # For now, we'll create the table structure without the actual extension
        print("✓ Vector extension placeholder (sqlite-vec would be loaded here)")

    def _create_tables(self) -> None:
        """Create all required database tables."""

        # Core rules table
        self.connection.execute(
            """
            CREATE TABLE rules (
                rule_id TEXT PRIMARY KEY,
                rule_number TEXT NOT NULL,
                rule_text TEXT NOT NULL,
                category TEXT NOT NULL,
                effective_date DATE,
                version INTEGER DEFAULT 1,
                rule_title TEXT,
                section TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        print("✓ Created rules table")

        # Full-text search virtual table
        self.connection.execute(
            """
            CREATE VIRTUAL TABLE rules_fts USING fts5(
                rule_id UNINDEXED,
                rule_number,
                rule_text,
                category,
                rule_title,
                content='rules',
                content_rowid='rowid'
            )
        """
        )
        print("✓ Created rules_fts full-text search table")

        # Vector embeddings table (placeholder structure)
        # In production, this would use sqlite-vec extension
        self.connection.execute(
            """
            CREATE TABLE vec_rules (
                rule_id TEXT PRIMARY KEY,
                embedding BLOB,
                dimension INTEGER DEFAULT 1536,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created vec_rules vector embeddings table")

        # Rule relationships and cross-references
        self.connection.execute(
            """
            CREATE TABLE rule_relationships (
                relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL,
                related_rule_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id),
                FOREIGN KEY (related_rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created rule_relationships table")

        # Historical rule versions
        self.connection.execute(
            """
            CREATE TABLE rule_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL,
                previous_text TEXT,
                change_description TEXT,
                changed_date DATE,
                version INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created rule_history table")

        # Violation patterns and triggers
        self.connection.execute(
            """
            CREATE TABLE violations (
                violation_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                violation_type TEXT NOT NULL,
                severity TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'DISQUALIFICATION')),
                penalty_description TEXT,
                trigger_patterns TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created violations table")

        # Analyzed scenarios for learning
        self.connection.execute(
            """
            CREATE TABLE scenarios (
                scenario_id TEXT PRIMARY KEY,
                scenario_text TEXT NOT NULL,
                analysis_result TEXT,
                applicable_rules TEXT,
                confidence_score REAL,
                embedding BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        print("✓ Created scenarios table")

        # Rule interpretations and official guidance
        self.connection.execute(
            """
            CREATE TABLE rule_interpretations (
                interpretation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL,
                interpretation_text TEXT NOT NULL,
                source TEXT,
                official_guidance BOOLEAN DEFAULT FALSE,
                effective_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created rule_interpretations table")

        # Compliance requirements for different meet types
        self.connection.execute(
            """
            CREATE TABLE compliance_requirements (
                requirement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                meet_type TEXT NOT NULL,
                requirement_text TEXT NOT NULL,
                category TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                mandatory BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        print("✓ Created compliance_requirements table")

        # Stroke-specific violations
        self.connection.execute(
            """
            CREATE TABLE stroke_violations (
                violation_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                stroke_type TEXT NOT NULL CHECK (stroke_type IN ('FREESTYLE', 'BACKSTROKE',
                'BREASTSTROKE', 'BUTTERFLY', 'INDIVIDUAL_MEDLEY')),
                trigger_pattern TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created stroke_violations table")

        # Timing-related violations
        self.connection.execute(
            """
            CREATE TABLE timing_violations (
                violation_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                timing_category TEXT NOT NULL,
                trigger_pattern TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created timing_violations table")

        # Equipment-related violations
        self.connection.execute(
            """
            CREATE TABLE equipment_violations (
                violation_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                equipment_type TEXT NOT NULL,
                trigger_pattern TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rule_id) REFERENCES rules(rule_id)
            )
        """
        )
        print("✓ Created equipment_violations table")

    def _create_indices(self) -> None:
        """Create database indices for optimal query performance."""

        # Performance indexes for rules table
        self.connection.execute("CREATE INDEX idx_rules_category ON rules(category)")
        self.connection.execute("CREATE INDEX idx_rules_version ON rules(version)")
        self.connection.execute("CREATE INDEX idx_rules_section ON rules(section)")
        self.connection.execute("CREATE INDEX idx_rules_number ON rules(rule_number)")
        print("✓ Created rules table indices")

        # Indexes for violations table
        self.connection.execute("CREATE INDEX idx_violations_type ON violations(violation_type)")
        self.connection.execute("CREATE INDEX idx_violations_severity ON violations(severity)")
        self.connection.execute("CREATE INDEX idx_violations_rule_id ON violations(rule_id)")
        print("✓ Created violations table indices")

        # Indexes for scenarios table
        self.connection.execute("CREATE INDEX idx_scenarios_created ON scenarios(created_at)")
        self.connection.execute("CREATE INDEX idx_scenarios_confidence ON scenarios(confidence_score)")
        print("✓ Created scenarios table indices")

        # Indexes for rule relationships
        self.connection.execute("CREATE INDEX idx_relationships_rule_id ON rule_relationships(rule_id)")
        self.connection.execute("CREATE INDEX idx_relationships_related_id ON rule_relationships(related_rule_id)")
        self.connection.execute("CREATE INDEX idx_relationships_type ON rule_relationships(relationship_type)")
        print("✓ Created rule_relationships table indices")

        # Indexes for rule history
        self.connection.execute("CREATE INDEX idx_history_rule_id ON rule_history(rule_id)")
        self.connection.execute("CREATE INDEX idx_history_version ON rule_history(version)")
        print("✓ Created rule_history table indices")

        # Indexes for interpretations
        self.connection.execute("CREATE INDEX idx_interpretations_rule_id ON rule_interpretations(rule_id)")
        self.connection.execute("CREATE INDEX idx_interpretations_official ON rule_interpretations(official_guidance)")
        print("✓ Created rule_interpretations table indices")

        # Indexes for compliance requirements
        self.connection.execute("CREATE INDEX idx_compliance_meet_type ON compliance_requirements(meet_type)")
        self.connection.execute("CREATE INDEX idx_compliance_priority ON compliance_requirements(priority)")
        print("✓ Created compliance_requirements table indices")

        # Indexes for stroke violations
        self.connection.execute("CREATE INDEX idx_stroke_violations_type ON stroke_violations(stroke_type)")
        self.connection.execute("CREATE INDEX idx_stroke_violations_rule_id ON stroke_violations(rule_id)")
        print("✓ Created stroke_violations table indices")

        # Indexes for timing violations
        self.connection.execute("CREATE INDEX idx_timing_violations_category ON timing_violations(timing_category)")
        self.connection.execute("CREATE INDEX idx_timing_violations_rule_id ON timing_violations(rule_id)")
        print("✓ Created timing_violations table indices")

        # Indexes for equipment violations
        self.connection.execute("CREATE INDEX idx_equipment_violations_type ON equipment_violations(equipment_type)")
        self.connection.execute("CREATE INDEX idx_equipment_violations_rule_id ON equipment_violations(rule_id)")
        print("✓ Created equipment_violations table indices")

    def _create_triggers(self) -> None:
        """Create database triggers for maintaining data consistency."""

        # Trigger to update FTS index when rules are inserted
        self.connection.execute(
            """
            CREATE TRIGGER rules_fts_insert AFTER INSERT ON rules
            BEGIN
                INSERT INTO rules_fts(rule_id, rule_number, rule_text, category, rule_title)
                VALUES (NEW.rule_id, NEW.rule_number, NEW.rule_text, NEW.category, NEW.rule_title);
            END
        """
        )

        # Trigger to update FTS index when rules are updated
        self.connection.execute(
            """
            CREATE TRIGGER rules_fts_update AFTER UPDATE ON rules
            BEGIN
                UPDATE rules_fts
                SET rule_number = NEW.rule_number,
                    rule_text = NEW.rule_text,
                    category = NEW.category,
                    rule_title = NEW.rule_title
                WHERE rule_id = NEW.rule_id;
            END
        """
        )

        # Trigger to remove from FTS index when rules are deleted
        self.connection.execute(
            """
            CREATE TRIGGER rules_fts_delete AFTER DELETE ON rules
            BEGIN
                DELETE FROM rules_fts WHERE rule_id = OLD.rule_id;
            END
        """
        )

        # Trigger to create rule history when rules are updated
        self.connection.execute(
            """
            CREATE TRIGGER rules_history_update AFTER UPDATE ON rules
            WHEN OLD.rule_text != NEW.rule_text OR OLD.rule_number != NEW.rule_number
            BEGIN
                INSERT INTO rule_history(rule_id, previous_text, change_description, changed_date, version)
                VALUES (OLD.rule_id, OLD.rule_text, 'Rule updated', date('now'), OLD.version);
            END
        """
        )

        print("✓ Created database triggers")

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

        # Set auto vacuum mode
        self.connection.execute("PRAGMA auto_vacuum=INCREMENTAL")

        print("✓ Configured database settings")

    def verify_database(self) -> bool:
        """Verify that all tables and indices were created successfully.

        Returns:
            bool: True if verification passes, False otherwise
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Check that all tables exist
            expected_tables = [
                "rules",
                "rules_fts",
                "vec_rules",
                "rule_relationships",
                "rule_history",
                "violations",
                "scenarios",
                "rule_interpretations",
                "compliance_requirements",
                "stroke_violations",
                "timing_violations",
                "equipment_violations",
            ]

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]

            missing_tables = set(expected_tables) - set(existing_tables)
            if missing_tables:
                print(f"✗ Missing tables: {missing_tables}")
                return False

            print("✓ All tables exist")

            # Check that indices exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indices = [row[0] for row in cursor.fetchall()]

            if len(indices) < 10:  # We created many indices
                print(f"✗ Expected more indices, found {len(indices)}")
                return False

            print(f"✓ Found {len(indices)} indices")

            # Check that triggers exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
            triggers = [row[0] for row in cursor.fetchall()]

            if len(triggers) < 3:  # We created 4 triggers
                print(f"✗ Expected more triggers, found {len(triggers)}")
                return False

            print(f"✓ Found {len(triggers)} triggers")

            connection.close()
            return True

        except sqlite3.Error as e:
            print(f"✗ Verification failed: {e}")
            return False


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
