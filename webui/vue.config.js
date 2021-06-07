// module.exports = {
//     devServer: {
//         '/service': {
//             // target: 'http://dungbeetles.xyz:60000/',
//             target: 'localhost:60000/',
//             // secure: false,
//             changeOrigin: true,
//             pathRewrite: {
//                 '^/service': '',
//             },
//         },
//     }
// }



module.exports = {
    devServer: {
        proxy: {
            '/service': {
                // target: 'http://dungbeetles.xyz:60000/',
                target: 'localhost:60000/',
                changeOrigin: true,
                pathRewrite: {
                    '^/service': '/sadfafsd'
                }
            }
        }
    }
}