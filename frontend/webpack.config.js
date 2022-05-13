const path = require('path');
module.exports = {
  // context: path.resolve(__dirname, "src"),
  entry: {
    'ChemicalSearchPage': path.resolve(__dirname, 'src', 'ChemicalSearchPageApp.js'),
    'ChemicalBlendPage': path.resolve(__dirname, 'src', 'ChemicalBlendPageApp.js'),
  },
  output: {
    path: path.resolve(__dirname, 'build', 'static', 'frontend'),
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              query: {
                name: 'assets/[name].[ext]'
              }
            }
          },
          {
            loader: 'image-webpack-loader',
            options: {
              query: {
                mozjpeg: {
                  progressive: true,
                },
                gifsicle: {
                  interlaced: true,
                },
                optipng: {
                  optimizationLevel: 7,
                }
              }
            }
          }]
      }
    ]
  }
};
