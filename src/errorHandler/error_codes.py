class handlerCode:
    def __init__(self, code, description, message):
        self.code = code
        self.description = description
        self.message = message

class codes:
    # Success Codes
    SUCCESS = handlerCode(200, "Success", "The request was successfully processed.")
    CREATED = handlerCode(201, "Created", "The resource was successfully created.")
    ACCEPTED = handlerCode(202, "Accepted", "The request has been accepted for processing.")
    NO_CONTENT = handlerCode(204, "No Content", "The request was successfully processed but no content is returned.")

    # Client Error Codes
    BAD_REQUEST = handlerCode(400, "Bad Request", "The request could not be understood or was missing required parameters.")
    UNAUTHORIZED = handlerCode(401, "Unauthorized", "Authentication is required and has failed or has not yet been provided.")
    FORBIDDEN = handlerCode(403, "Forbidden", "You do not have permission to access this resource.")
    NOT_FOUND = handlerCode(404, "Not Found", "The requested resource could not be found.")
    METHOD_NOT_ALLOWED = handlerCode(405, "Method Not Allowed", "The requested method is not allowed for the specified resource.")
    CONFLICT = handlerCode(409, "Conflict", "The request could not be completed due to a conflict with the current state of the resource.")
    PAYLOAD_TOO_LARGE = handlerCode(413, "Payload Too Large", "The request payload is too large to be processed.")
    UNSUPPORTED_MEDIA_TYPE = handlerCode(415, "Unsupported Media Type", "The request payload format is not supported.")
    UNPROCESSABLE_ENTITY = handlerCode(422, "Unprocessable Entity", "The request was well-formed but could not be followed due to semantic errors.")
    INVALID_STEP = handlerCode(423, "Invalid step", "step not suported")
    TOO_MANY_REQUESTS = handlerCode(429, "Too Many Requests", "The user has sent too many requests in a given amount of time.")

    # Server Error Codes
    INTERNAL_SERVER_ERROR = handlerCode(500, "Internal Server Error", "An unexpected error occurred.")
    NOT_IMPLEMENTED = handlerCode(501, "Not Implemented", "The requested functionality is not implemented.")
    BAD_GATEWAY = handlerCode(502, "Bad Gateway", "The server received an invalid response from the upstream server.")
    SERVICE_UNAVAILABLE = handlerCode(503, "Service Unavailable", "The server is currently unable to handle the request due to a temporary overload or maintenance.")
    GATEWAY_TIMEOUT = handlerCode(504, "Gateway Timeout", "The server did not receive a timely response from the upstream server.")
