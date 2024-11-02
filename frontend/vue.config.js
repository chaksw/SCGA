const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
    transpileDependencies: true,
});

// 配置代理，解决跨域问题
module.exports = {
    devServer: {
        proxy: {
            '/api/': {
                target: `http://127.0.0.1:8000/api`, // 后段 API 服务器地址
                changeOrigin: true, // 改变请求的源头，解决跨域问题
                pathRewrite: {
                    '^/api': '', // 将 "/api" 前缀移除
                },
            },
        },
    },
};
