import ConfigParser


class Config:
	site_config = ConfigParser.ConfigParser()
	site_config.read("config.ini")

	def get_db_host(self):
		return self.site_config.get('Database', 'db.host');

	def get_db_password(self):
		return self.site_config.get('Database', 'db.password');

	def get_db_name(self):
		return self.site_config.get('Database', 'db.name');

	def get_db_user(self):
		return self.site_config.get('Database', 'db.user');
	
	def get_telegram_token(self):
		return self.site_config.get('Telegram', 'telegram.token');
