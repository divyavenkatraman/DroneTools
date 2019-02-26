import pandas as pd

class FileReader:
	def read_csv(self, fname):
		return pd.read_csv(fname).values
	

