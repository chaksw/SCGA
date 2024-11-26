import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
	plugins: [vue()],
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
		},
	},
	server: {
		proxy: {
			"/api/": {
				target: `http://127.0.0.1:8000/`, // 后端 API 服务器地址
				changeOrigin: true, // 改变请求的源头，解决跨域问题
				pathRewrite: {
					"^/api": "", // 将 "/api" 前缀移除
				},
			},
		},
	},
});
