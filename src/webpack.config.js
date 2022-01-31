const path = require("path");
const webpack = require("webpack");

var fs = require("fs");
var text = fs.readFileSync("./__init__.py");

const regex = /[0-9]\d*(\.[0-9]\d*){0,3}/m;

let m;
let version="0.0.0";

if ((m = regex.exec(text)) !== null) {
    // The result can be accessed through the `m`-variable.
    version = m[0]
}

version = version.replaceAll(".", "-");

console.log(version)

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "./static/invoices"),
    filename: "invoices-[name]-" + version + ".js",
  },
  module: {
    rules: [
      {
        test: /\.js|.jsx$/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        NODE_ENV: JSON.stringify("development"),
      },
    }),
  ],
};
