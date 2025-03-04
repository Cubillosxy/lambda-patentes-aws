test "api_gateway_url_test" {
  description = "Verify that the API URL output contains the expected execute-api domain"

  input = {
    api_url = output.api_url.value
  }

  assertion {
    condition     = contains(input.api_url, "execute-api")
    error_message = "The API URL does not appear to be valid; it should contain 'execute-api'"
  }
}
