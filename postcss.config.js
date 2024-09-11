module.exports = {
    plugins: [
      require('postcss-preset-env')({
        // Configurações do PostCSS
      }),
      require('cssnano') // Minifica o CSS
    ],
  };
  