const path = require("path");

module.exports = {
  mode: "development", // Change to 'production' for deployment
  entry: path.resolve(__dirname, "chatbot/static/js/chat.ts"), // Corrected TS file location
  output: {
    filename: "chat.js",
    path: path.resolve(__dirname, "chatbot/static/js"), // Output directory
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [".ts", ".js"],
  },
};
