require('dotenv').config()
const express = require('express')

const app = express()
const port = process.env.PORT

app.listen(port, () => {
    console.log(`[server]: Server is running at http://localhost:${port}`)
});