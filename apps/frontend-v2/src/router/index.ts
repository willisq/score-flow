import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: () => import("@/layout/AppLayout.vue"),
      children: [
        {
          path: "",
          name: "dashboard",
          component: () => import("@/features/dashboard/views/DashboardView.vue"),
        },
        {
          path: "competitors",
          name: "competitors",
          component: () => import("@/features/registration/views/CompetitorListView.vue"),
        },
        {
          path: "academies",
          name: "academies",
          component: () => import("@/features/registration/views/AcademyListView.vue"),
        },
        {
          path: "tournaments",
          name: "tournaments",
          component: () => import("@/features/tournament/views/TournamentListView.vue"),
        },
        {
          path: "categories",
          name: "categories",
          component: () => import("@/features/tournament/views/CategoryListView.vue"),
        },
        {
          path: "rank-groups",
          name: "rank-groups",
          component: () => import("@/features/tournament/views/RankGroupListView.vue"),
        },
        {
          path: "enrollment",
          name: "enrollment",
          component: () => import("@/features/tournament/views/CategoryEnrollmentView.vue"),
        },
        {
          path: "category-builder",
          name: "category-builder",
          component: () => import("@/features/tournament/views/CategoryBuilderView.vue"),
        },
        {
          path: "brackets",
          name: "brackets",
          component: () => import("@/features/bracket/views/BracketView.vue"),
        },
      ],
    },
  ],
});

export default router;
