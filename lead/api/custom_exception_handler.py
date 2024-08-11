from rest_framework.views import exception_handler
import logging
def custom_exception_handler(exc, context):
    # Call DRF's default exception handler to get the standard error response
    response = exception_handler(exc, context)
    logging.error("Custom exception handler triggered.")  # Test logging
    if response is not None:
        # Convert list errors to a single string if 'detail' key is present
        if 'detail' in response.data:
            response.data['detail'] = response.data['detail'][0] if isinstance(response.data['detail'], list) else response.data['detail']
        else:
            # For other keys that might have list errors
            for key, value in response.data.items():
                if isinstance(value, list):
                    response.data[key] = value[0]  # Convert list to a single string

        # Customize the error format as needed
        response.data = {
            'error': {
                'code': response.status_code,
                'message': response.data
            }
        }

    return response
