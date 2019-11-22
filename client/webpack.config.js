const path = require('path');
const webpack = require('webpack');
const bundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: path.join(__dirname, 'src/index'),

    output: {
        path: path.join(__dirname, 'dist'),
        filename: '[name]-[hash].js'
    },

    plugins: [
        new bundleTracker({
            path: __dirname,
            filename: 'webpack-stats.json'
        }),
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // all options are optional
            filename: '[name]-[hash].css',
            chunkFilename: '[id]-[hash].css',
            ignoreOrder: false, // Enable to remove warnings about conflicting order
          }),
    ],

    module: {
        rules: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.(sa|sc|c)ss$/,
                exclude: [
                    /\.png$/,
                    /\.jpe?g$/,
                ],
                
                use: [
                  {
                    loader: MiniCssExtractPlugin.loader,
                    options: {
                      hmr: process.env.NODE_ENV === 'development',
                    },
                  },
                  'sass-loader',
                  'css-loader',
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
            }
        ],
    },
}