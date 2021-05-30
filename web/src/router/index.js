import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const routes = [{
		path: '*',
		redirect: '/home'
	},
	{
		name: 'home',
		redirect: '/home',
		component: () => import('../view/home'),
		children: [{
			name: 'home',
			path: '/home',
			component: () => import('../view/home'),
			meta: {
				title: ''
			}
		}, ]
	}
];

// add route path
routes.forEach(route => {
	route.path = route.path || '/' + (route.name || '');
});

const router = new Router({
	routes
});

router.beforeEach((to, from, next) => {
	const title = to.meta && to.meta.title;
	if (title) {
		document.title = title;
	}
	next();
});

export {
	router
};
