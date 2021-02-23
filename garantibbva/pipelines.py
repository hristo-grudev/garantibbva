import re
import sqlite3


class GarantibbvaPipeline:
    conn = sqlite3.connect('garantibbva.db')
    cursor = conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `garantibbva` (
                                                                        title varchar(100),
                                                                        description text
                                                                        )''')
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            title = item['title']
            title = re.sub('"', "'", title).strip()
        except:
            title = ''
        try:
            description = item['description']
            description = re.sub('"', "'", description).strip()
        except:
            description = ''


        self.cursor.execute(f'''select * from garantibbva where title = "{title}"''')
        is_exist = self.cursor.fetchall()

        if len(is_exist) == 0:
            self.cursor.execute(
                f'''insert into `garantibbva` (`title`, `description`) values ("{title}", "{description}")''')
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
