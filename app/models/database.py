import json
import sqlite3
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "export_manager.db")

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Listings table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id TEXT PRIMARY KEY,
                created_at TEXT,
                updated_at TEXT,
                raw_input TEXT,
                normalized_text TEXT,
                target_platform TEXT,
                target_country TEXT,
                attributes_json TEXT,
                slots_status_json TEXT,
                listing_json TEXT,
                quality_score_json TEXT,
                market_insight_json TEXT,
                status TEXT,
                published_platforms_json TEXT
            )
            """)

            # Buyer inquiries table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS buyer_inquiries (
                id TEXT PRIMARY KEY,
                listing_id TEXT,
                buyer_name TEXT,
                buyer_country TEXT,
                inquiry_message TEXT,
                intent TEXT,
                catalog_answerable INTEGER,
                requires_exporter INTEGER,
                exporter_question_urdu TEXT,
                exporter_reply_urdu TEXT,
                generated_reply_en TEXT,
                status TEXT,
                created_at TEXT,
                FOREIGN KEY (listing_id) REFERENCES listings (id)
            )
            """)

            # Exporter users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                full_name TEXT,
                city TEXT,
                cluster TEXT,
                created_at TEXT
            )
            """)

            # Seed default demo exporter user
            cursor.execute("SELECT COUNT(*) as count FROM users")
            if cursor.fetchone()["count"] == 0:
                cursor.execute("""
                INSERT INTO users (id, username, full_name, city, cluster, created_at)
                VALUES ('user-coretech-01', 'sufyan_exporter', 'Sufyan Arain (CoreTech Exporter)', 'Sialkot', 'Leather & Surgical Hub', datetime('now'))
                """)

            conn.commit()

    def save_listing(self, data: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO listings (
                id, created_at, updated_at, raw_input, normalized_text,
                target_platform, target_country, attributes_json, slots_status_json,
                listing_json, quality_score_json, market_insight_json, status,
                published_platforms_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                updated_at=excluded.updated_at,
                raw_input=excluded.raw_input,
                normalized_text=excluded.normalized_text,
                target_platform=excluded.target_platform,
                target_country=excluded.target_country,
                attributes_json=excluded.attributes_json,
                slots_status_json=excluded.slots_status_json,
                listing_json=excluded.listing_json,
                quality_score_json=excluded.quality_score_json,
                market_insight_json=excluded.market_insight_json,
                status=excluded.status,
                published_platforms_json=excluded.published_platforms_json
            """, (
                data["id"],
                data["created_at"],
                data["updated_at"],
                data.get("raw_input", ""),
                data.get("normalized_text", ""),
                data.get("target_platform", "alibaba"),
                data.get("target_country", "USA"),
                json.dumps(data.get("attributes", {})),
                json.dumps(data.get("slots_status", {})),
                json.dumps(data.get("listing", {})) if data.get("listing") else None,
                json.dumps(data.get("quality_score", {})) if data.get("quality_score") else None,
                json.dumps(data.get("market_insight", {})) if data.get("market_insight") else None,
                data.get("status", "draft"),
                json.dumps(data.get("published_platforms", {}))
            ))
            conn.commit()

    def get_listing(self, listing_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM listings WHERE id = ?", (listing_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row["id"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "raw_input": row["raw_input"],
                "normalized_text": row["normalized_text"],
                "target_platform": row["target_platform"],
                "target_country": row["target_country"],
                "attributes": json.loads(row["attributes_json"] or "{}"),
                "slots_status": json.loads(row["slots_status_json"] or "{}"),
                "listing": json.loads(row["listing_json"]) if row["listing_json"] else None,
                "quality_score": json.loads(row["quality_score_json"]) if row["quality_score_json"] else None,
                "market_insight": json.loads(row["market_insight_json"]) if row["market_insight_json"] else None,
                "status": row["status"],
                "published_platforms": json.loads(row["published_platforms_json"] or "{}")
            }

    def list_all_listings(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM listings ORDER BY created_at DESC")
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row["id"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "raw_input": row["raw_input"],
                    "normalized_text": row["normalized_text"],
                    "target_platform": row["target_platform"],
                    "target_country": row["target_country"],
                    "attributes": json.loads(row["attributes_json"] or "{}"),
                    "slots_status": json.loads(row["slots_status_json"] or "{}"),
                    "listing": json.loads(row["listing_json"]) if row["listing_json"] else None,
                    "quality_score": json.loads(row["quality_score_json"]) if row["quality_score_json"] else None,
                    "market_insight": json.loads(row["market_insight_json"]) if row["market_insight_json"] else None,
                    "status": row["status"],
                    "published_platforms": json.loads(row["published_platforms_json"] or "{}")
                })
            return results

    def save_inquiry(self, inquiry: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO buyer_inquiries (
                id, listing_id, buyer_name, buyer_country, inquiry_message,
                intent, catalog_answerable, requires_exporter,
                exporter_question_urdu, exporter_reply_urdu,
                generated_reply_en, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                exporter_reply_urdu=excluded.exporter_reply_urdu,
                generated_reply_en=excluded.generated_reply_en,
                status=excluded.status
            """, (
                inquiry["id"],
                inquiry["listing_id"],
                inquiry["buyer_name"],
                inquiry["buyer_country"],
                inquiry["inquiry_message"],
                inquiry["intent"],
                1 if inquiry.get("catalog_answerable") else 0,
                1 if inquiry.get("requires_exporter") else 0,
                inquiry.get("exporter_question_urdu"),
                inquiry.get("exporter_reply_urdu"),
                inquiry.get("generated_reply_en"),
                inquiry.get("status", "pending"),
                inquiry.get("created_at", datetime.now().isoformat())
            ))
            conn.commit()

    def get_inquiries_for_listing(self, listing_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM buyer_inquiries WHERE listing_id = ? ORDER BY created_at DESC", (listing_id,))
            rows = cursor.fetchall()
            return [
                {
                    "id": r["id"],
                    "listing_id": r["listing_id"],
                    "buyer_name": r["buyer_name"],
                    "buyer_country": r["buyer_country"],
                    "inquiry_message": r["inquiry_message"],
                    "intent": r["intent"],
                    "catalog_answerable": bool(r["catalog_answerable"]),
                    "requires_exporter": bool(r["requires_exporter"]),
                    "exporter_question_urdu": r["exporter_question_urdu"],
                    "exporter_reply_urdu": r["exporter_reply_urdu"],
                    "generated_reply_en": r["generated_reply_en"],
                    "status": r["status"],
                    "created_at": r["created_at"]
                }
                for r in rows
            ]

    def get_inquiry(self, inquiry_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM buyer_inquiries WHERE id = ?", (inquiry_id,))
            r = cursor.fetchone()
            if not r:
                return None
            return {
                "id": r["id"],
                "listing_id": r["listing_id"],
                "buyer_name": r["buyer_name"],
                "buyer_country": r["buyer_country"],
                "inquiry_message": r["inquiry_message"],
                "intent": r["intent"],
                "catalog_answerable": bool(r["catalog_answerable"]),
                "requires_exporter": bool(r["requires_exporter"]),
                "exporter_question_urdu": r["exporter_question_urdu"],
                "exporter_reply_urdu": r["exporter_reply_urdu"],
                "generated_reply_en": r["generated_reply_en"],
                "status": r["status"],
                "created_at": r["created_at"]
            }

db = Database()
