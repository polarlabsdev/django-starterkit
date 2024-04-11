import uuid


def generate_request_id():
	return uuid.uuid4().hex
