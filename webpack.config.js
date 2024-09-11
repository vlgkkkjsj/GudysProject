const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  mode: 'production', // Certifique-se de estar no modo de produção para otimização
  entry: './static/scripts/script.js', // Seu ponto de entrada JavaScript
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'staticfiles'), // Saída para o diretório `staticfiles`
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader, // Extrai o CSS em arquivos separados
          'css-loader', // Interpreta o @import e url()
          'postcss-loader', // Processa o CSS com PostCSS
        ],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'styles.min.css', // Nome do arquivo CSS minificado
    }),
  ],
  optimization: {
    minimize: true,
    minimizer: [
      new CssMinimizerPlugin(), // Minifica o CSS
    ],
  },
};
