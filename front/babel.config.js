const prodPlugins = []
if (process.env.NODE_ENV === 'production'){
  prodPlugins.push('transform-remove-console')
}


module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  plugins: [
    [
      'component',
      {
        libraryName: 'element-ui',
        styleLibraryName: 'theme-chalk'
      }
    ],
    // 数组里的每一项展开放入
    ...prodPlugins
  ]
}
