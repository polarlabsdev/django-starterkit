from core.utils.tavern import check_response, gen_obj_schema_definition


def verify_tags_shape(response):
	"""
	Function to verify the shape of the tags endpoint with tavern
	"""
	print('Verifying tags response with tavern...')

	expected_props = {
		'next': {'type': ['string', 'null']},
		'previous': {'type': ['string', 'null']},
		'count': {'type': 'number'},
		'results': {
			'type': 'array',
			'items': {
				'type': 'object',
				'properties': {
					'name': {'type': 'string'},
					'slug': {'type': 'string'},
					'colour': {'type': 'string'},
				},
			},
		},
	}

	schema = gen_obj_schema_definition(expected_props)

	check_response(response, schema=schema)


def verify_list_shape(response):
	"""
	Function to verify the shape of the blog endpoint with tavern
	"""
	print('Verifying blog response with tavern...')

	tag_props = {
		'name': {'type': 'string'},
		'slug': {'type': 'string'},
		'color': {'type': 'string'},
	}

	results_props = {
		'name': {'type': 'string'},
		'slug': {'type': 'string'},
		'summary': {'type': 'string'},
		'tags': {
			'type': 'array',
			'items': gen_obj_schema_definition(tag_props),
		},
		'thumbnail': {'type': 'string'},
		'read_time': {'type': 'string'},
		'created': {'type': 'string'},
		'updated': {'type': 'string'},
	}

	expected_props = {
		'next': {'type': ['string', 'null']},
		'previous': {'type': ['string', 'null']},
		'count': {'type': 'number'},
		'results': {
			'type': 'array',
			'items': gen_obj_schema_definition(results_props),
		},
	}

	schema = gen_obj_schema_definition(expected_props)

	check_response(response, schema=schema)
