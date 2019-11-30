module.exports = {
    entry: './frontend/src/index.jsx',
    output: {
      filename: 'main.js',
      path: __dirname + '/frontend/static/frontend'
    },
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        }
      ]
    }
  };