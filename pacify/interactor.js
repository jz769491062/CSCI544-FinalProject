const axios = require("axios")
const server = "http://127.0.0.1:5000/check"

module.exports = {

    getEvaluation: async function(msg) {
        url = server+"?msg="+msg
        try {
          const response = await axios.get(url);
          console.log(response.data)
          return response.data;
        } catch (err) {
          console.log(err);
        }
      }
}