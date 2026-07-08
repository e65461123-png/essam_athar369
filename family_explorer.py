#!/usr/bin/env python3
"""
👨‍👩‍👧‍👦 المستكشف العائلي الذكي - AI Builder Hub
ابحث عن جذورك واكتشف قصص أجدادك
"""

import json
import random
import time
import os
from datetime import datetime

class FamilyExplorer:
    def __init__(self):
        self.family_data = {}
        self.stories = []
        self.load_data()

    def load_data(self):
        """تحميل البيانات السابقة"""
        if os.path.exists("family_data.json"):
            with open("family_data.json", "r") as f:
                self.family_data = json.load(f)

    def save_data(self):
        """حفظ البيانات"""
        with open("family_data.json", "w") as f:
            json.dump(self.family_data, f, indent=4)

    def add_family_member(self, name, relation, birth_year=None, birth_place=None):
        """إضافة فرد جديد للعائلة"""
        member = {
            "name": name,
            "relation": relation,
            "birth_year": birth_year,
            "birth_place": birth_place,
            "stories": []
        }
        
        if relation not in self.family_data:
            self.family_data[relation] = []
        self.family_data[relation].append(member)
        self.save_data()
        print(f"✅ تم إضافة {name} كـ {relation}")

    def search_family(self, family_name, place):
        """محاكاة البحث عن العائلة"""
        print(f"\n🔍 جاري البحث عن عائلة {family_name} في {place}...")
        time.sleep(2)
        
        # محاكاة النتائج
        results = {
            "family": family_name,
            "place": place,
            "records_found": random.randint(1, 10),
            "oldest_record": random.randint(1850, 1900),
            "family_members": [
                {"name": f"{family_name} الأكبر", "role": "الجد الأكبر", "year": random.randint(1850, 1900)},
                {"name": f"{family_name} الأوسط", "role": "الجد", "year": random.randint(1890, 1920)},
                {"name": f"{family_name} الأصغر", "role": "الأب", "year": random.randint(1920, 1950)}
            ]
        }
        
        print(f"📊 تم العثور على {results['records_found']} سجل")
        print(f"📜 أقدم سجل يعود لـ {results['oldest_record']}")
        
        return results

    def generate_story(self, member_name, year, place):
        """توليد قصة افتراضية عن الجد"""
        stories = [
            f"في سنة {year}، كان {member_name} يعيش في {place} ويعمل في الزراعة. كان معروفاً بحكمته وكرمه.",
            f"{member_name} كان تاجراً متنقلاً في {place}. سافر إلى العديد من القرى وبنى سمعة طيبة.",
            f"اشتهر {member_name} في {place} بمعرفته بالطب الشعبي. كان يعالج الناس بالأعشاب.",
            f"{member_name} كان شاعراً في {place}. نظم قصائد عن الحياة والطبيعة التي لا تزال تُتداول.",
            f"عُرف عن {member_name} شجاعته في الدفاع عن قريته {place}. كان مقاتلاً شرساً وحكيماً."
        ]
        return random.choice(stories)

    def build_family_tree(self):
        """بناء شجرة العائلة"""
        print("\n🌳 بناء شجرة العائلة...")
        time.sleep(1)
        
        tree = """
        ╔══════════════════════════════════════════════════════════╗
        ║                    شجرة العائلة                        ║
        ║                                                        ║
        ║                       👴                               ║
        ║                  الجد الأكبر                          ║
        ║                    │                                   ║
        ║                       👨                              ║
        ║                      الجد                             ║
        ║                    │                                   ║
        ║                       👨                              ║
        ║                     الأب                              ║
        ║                    │                                   ║
        ║                       👦                              ║
        ║                     الابن                             ║
        ║                                                        ║
        ║   📍 المكان: أم القصور - منفلوط - أسيوط              ║
        ║   🏷️ العائلة: الكومي                                ║
        ╚══════════════════════════════════════════════════════════╝
        """
        print(tree)

    def show_family_stories(self):
        """عرض قصص العائلة"""
        print("\n📖 قصص العائلة:")
        for relation, members in self.family_data.items():
            for member in members:
                if member.get("stories"):
                    for story in member["stories"]:
                        print(f"   • {story}")

def main():
    explorer = FamilyExplorer()
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   👨‍👩‍👧‍👦 المستكشف العائلي الذكي                         ║
    ║   ابحث عن جذورك واكتشف قصص أجدادك                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n📋 **القائمة الرئيسية:**")
        print("1. إضافة فرد جديد للعائلة")
        print("2. البحث عن عائلة")
        print("3. عرض شجرة العائلة")
        print("4. توليد قصة عن جد")
        print("5. عرض جميع القصص")
        print("6. حفظ البيانات")
        print("7. خروج")
        
        choice = input("\n🔮 اختر خيار (1-7): ")
        
        if choice == "1":
            name = input("👤 اسم الفرد: ")
            relation = input("🔗 الصلة (جد، أب، ابن، إلخ): ")
            year = input("📅 سنة الميلاد (اختياري): ")
            place = input("📍 مكان الميلاد (اختياري): ")
            explorer.add_family_member(name, relation, year or None, place or None)
        
        elif choice == "2":
            family_name = input("🏷️ اسم العائلة: ")
            place = input("📍 المكان: ")
            results = explorer.search_family(family_name, place)
            
            # إضافة النتائج للشجرة
            for member in results["family_members"]:
                explorer.add_family_member(member["name"], member["role"], member["year"])
        
        elif choice == "3":
            explorer.build_family_tree()
        
        elif choice == "4":
            name = input("👤 اسم الجد: ")
            year = input("📅 السنة: ")
            place = input("📍 المكان: ")
            story = explorer.generate_story(name, year, place)
            print(f"\n📖 {story}")
            
            # حفظ القصة
            if name in explorer.family_data:
                for member in explorer.family_data[name]:
                    member["stories"].append(story)
            explorer.save_data()
        
        elif choice == "5":
            explorer.show_family_stories()
        
        elif choice == "6":
            explorer.save_data()
            print("✅ تم حفظ البيانات")
        
        elif choice == "7":
            print("👋 مع السلامة! استمر في اكتشاف جذورك.")
            break
        
        else:
            print("❌ اختيار غير صحيح")

if __name__ == "__main__":
    main()
