import sqlite3
import random
import logging
from typing import List, Tuple

# Database file name
# نام فایل دیتابیس
DB_NAME = 'homework.db'

# Constants for team levels
# ثابت‌ها برای سطوح تیم‌ها
LEVEL_STRONG = 'Strong'
LEVEL_MEDIUM = 'Medium'
LEVEL_WEAK = 'Weak'

def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    """
    Generates test data for UEFA draw based on the number of groups (4 to 16).
    داده‌های تست قرعه‌کشی یوفا را بر اساس تعداد گروه‌ها (۴ تا ۱۶) تولید می‌کند.
    """
    
    if not 4 <= number_of_groups <= 16:
        raise ValueError("Number of groups must be between 4 and 16.")
    
    # 1. Drop and create tables
    # 1. حذف و ایجاد جداول
    cursor.executescript("""
        DROP TABLE IF EXISTS uefa_commands;
        DROP TABLE IF EXISTS uefa_draw;
        
        CREATE TABLE uefa_commands (
            team_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            country TEXT,
            level TEXT NOT NULL
        );
        
        CREATE TABLE uefa_draw (
            team_id INTEGER,
            group_id INTEGER NOT NULL,
            FOREIGN KEY(team_id) REFERENCES uefa_commands(team_id)
        );
    """)
    
    # Number of teams required for each level
    # تعداد تیم‌های مورد نیاز برای هر سطح
    num_strong = number_of_groups
    num_medium = number_of_groups * 2
    num_weak = number_of_groups
    total_teams = num_strong + num_medium + num_weak

    # Helper lists for unique names and countries
    # لیست‌های کمکی برای نام‌ها و کشورهای منحصر به فرد
    team_names = [f"Team-{i+1}" for i in range(total_teams)]
    team_countries = [f"Country-{i+1}" for i in range(total_teams)] 
    random.shuffle(team_countries)

    # 2. Generate and insert data into uefa_commands
    # 2. تولید و درج داده در uefa_commands
    teams_data: List[Tuple[str, str, str]] = []
    
    # Helper to generate teams with specified level
    # تابع کمکی برای تولید تیم‌ها با سطح مشخص
    def generate_teams(count: int, level: str):
        for _ in range(count):
            name = team_names.pop(0)
            country = team_countries.pop(0)
            teams_data.append((name, country, level))

    generate_teams(num_strong, LEVEL_STRONG)
    generate_teams(num_medium, LEVEL_MEDIUM)
    generate_teams(num_weak, LEVEL_WEAK)
    
    # Insert into uefa_commands using executemany
    # درج در uefa_commands با استفاده از executemany
    cursor.executemany("""
        INSERT INTO uefa_commands (name, country, level) 
        VALUES (?, ?, ?)
    """, teams_data)
    
    # 3. Perform the draw and insert into uefa_draw
    # 3. انجام قرعه‌کشی و درج در uefa_draw
    
    # Retrieve all teams with their IDs and levels
    # بازیابی تمام تیم‌ها با ID و سطح آن‌ها
    cursor.execute("SELECT team_id, level FROM uefa_commands")
    all_teams = cursor.fetchall()
    
    # Group teams by level
    # دسته‌بندی تیم‌ها بر اساس سطح
    teams_by_level = {
        LEVEL_STRONG: [team[0] for team in all_teams if team[1] == LEVEL_STRONG],
        LEVEL_MEDIUM: [team[0] for team in all_teams if team[1] == LEVEL_MEDIUM],
        LEVEL_WEAK: [team[0] for team in all_teams if team[1] == LEVEL_WEAK],
    }
    
    # Shuffle teams within each level for randomness
    # در هم آمیختن تیم‌ها در هر سطح برای تصادفی بودن
    for level in teams_by_level:
        random.shuffle(teams_by_level[level])
        
    draw_data: List[Tuple[int, int]] = [] # (team_id, group_id)
    
    # Perform the draw
    # انجام قرعه‌کشی
    for group_id in range(1, number_of_groups + 1):
        # 1 Strong team
        draw_data.append((teams_by_level[LEVEL_STRONG].pop(), group_id))
        # 2 Medium teams
        draw_data.append((teams_by_level[LEVEL_MEDIUM].pop(), group_id))
        draw_data.append((teams_by_level[LEVEL_MEDIUM].pop(), group_id))
        # 1 Weak team
        draw_data.append((teams_by_level[LEVEL_WEAK].pop(), group_id))

    # Insert into uefa_draw using executemany
    # درج در uefa_draw با استفاده از executemany
    cursor.executemany("""
        INSERT INTO uefa_draw (team_id, group_id) 
        VALUES (?, ?)
    """, draw_data)
    
    logging.info(f"Successfully generated {total_teams} teams and performed draw for {number_of_groups} groups.")

# --- Main for Demonstration ---
# --- بخش اصلی برای نمایش ---
def main():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        NUM_GROUPS_TO_TEST = 8 # Test with 8 groups
        generate_test_data(cursor, NUM_GROUPS_TO_TEST)
        conn.commit()
        
        # Verify the draw
        # تأیید قرعه‌کشی
        cursor.execute("""
            SELECT 
                d.group_id, 
                c.level, 
                COUNT(*) as count 
            FROM 
                uefa_draw d
            JOIN 
                uefa_commands c ON d.team_id = c.team_id
            GROUP BY 
                d.group_id, 
                c.level
            ORDER BY 
                d.group_id, 
                c.level
        """)
        print("\nDraw verification (Group, Level, Count):")
        for row in cursor.fetchall():
            print(row)
        
if __name__ == '__main__':
    main()
