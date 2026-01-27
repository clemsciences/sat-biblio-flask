module.exports = {
    transpileDependencies: [
        'marked'
    ],
    devServer: {
        proxy: 'http://localhost:5000'
    }
}