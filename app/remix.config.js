/** @type {import('@remix-run/dev').AppConfig} */
export default {
  ignoredRouteFiles: ["**/.*"],
  appDirectory: "app",
  assetsBuildDirectory: "public/build",
  publicPath: "/build/",
  serverBuildPath: "build/index.js",
  serverDependenciesToBundle:  ['swiper', 'swiper/react', 'swiper/react/swiper-react.js', 'ssr-window','ssr-window/ssr-window.esm.js','dom7'],
  tailwind: true,
  postcss: true,
};
