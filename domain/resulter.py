class ResultStruct:
	def __init__(self, result_function, kwargs):
		self.data = kwargs
		self.default_data = kwargs
		self.result_function = result_function

	def get_results(self):
		return self.result_function(self.data)

	def add_result(self, result):
		self.data["count"] += 1
		self.data["passed"] += not result.value
		if not result.value:
			self.data["min_time"] = min(
					self.data["min_time"], result.additional_fields["_time"]
			)
			self.data["max_time"] = max(
					self.data["max_time"], result.additional_fields["_time"]
			)
			self.data["sum_t"] += result.additional_fields["_time"]

	def __str__(self):
		return "\n".join(f"{k}: {v}" for k, v in self.get_results().items())

	@staticmethod
	def default_config():
		yield lambda data: {
				"passed": data["passed"] / data["count"] if data[
					"count"] else 0,
				"min_time": data["min_time"] if data["min_time"] < float("inf") else "NaN",
				"max_time": data["max_time"] or "NaN",
				"average": round(data["sum_t"] / data["passed"], 2)
				if data["passed"]
				else "NaN",
				"count": data["count"],
		}
		yield {
				"passed": 0,
				"count": 0,
				"min_time": float("inf"),
				"max_time": 0,
				"sum_t": 0,
		}
