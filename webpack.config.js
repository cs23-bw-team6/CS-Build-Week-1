module.exports = {
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                  // Creates `style` nodes from JS strings
                  'style-loader',
                  // Translates CSS into CommonJS
                  'css-loader',
                  // Compiles Sass to CSS
                  'sass-loader',
                ],
            },
            {
                test: /\.(png|svg|jpg|gif|jpe?g)$/,
                use: [
                  {
                    options: {
                      name: "[name].[ext]",
                      outputPath: "images/"
                    },
                    loader: "url-loader"
                  }
                ]
            },
        ]
    }
};