<template>
    <div class="grid grid-cols-12 gap-8 grid-rows-4">
        <div class="col-span-12 row-span-4">
            <h1 class="text-6xl">Bienvenido</h1>
            <h5>Aqui podras crear competidores y sus categorias para armas de manera automatica las piramides de
                competencia</h5>

            <Timeline :value="events" align="alternate" class="customized-timeline">
                <template #marker="slotProps">
                    <span class="flex w-8 h-8 items-center justify-center text-white rounded-full z-10 shadow-sm"
                        :style="{ backgroundColor: slotProps.item.color }">
                        <i :class="slotProps.item.icon"></i>
                    </span>
                </template>
                <template #content="slotProps">
                    <Card class="mt-4">
                        <template #title>
                            {{ slotProps.item.status }}
                        </template>
                        <template #content>
                            <p>
                                {{ slotProps.item.description }}
                            </p>
                            <Button label="Ver mas" text><router-link :to="slotProps.item.link"
                                    class="layout-topbar-logo">Ver más</router-link></Button>
                        </template>
                    </Card>
                </template>
            </Timeline>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";

const events = ref([
    { status: 'Crea Categorias', date: '15/10/2020 10:30', icon: 'pi pi-users', color: '#9C27B0', description: "Genera las categorias que iran en la competencia, eligiendo las edades, alturas, rangos y otros detalles de la categoria.", link: '/category' },
    { status: 'Registra a los competidores', date: '15/10/2020 14:00', icon: 'pi pi-id-card', color: '#673AB7', description: "Al registrar a los competidores, automaticamente se clasificarán en sus categorías.", link: '/competitor' },
    { status: 'Genera las Piramides', date: '15/10/2020 16:15', icon: 'pi pi-users', color: '#FF9800', description: "Al consultar a los competidores que han sido clasificados en una categoria, puedes generar la piramide con solo un click.", link: '/category' },
    { status: 'Consulta las piramides', date: '16/10/2020 10:00', icon: 'pi pi-check', color: '#607D8B', description: "Una vez quue has generado las piramides, puedes consultar el resultado final en la interfaz de piramides. Si quieres volver a generar la piramide, lo puedes volver a hacer, incluso con nuevos competidores.", link: '/pyramid' }
]);

</script>

<style lang="scss" scoped>
@media screen and (max-width: 960px) {
    ::v-deep(.customized-timeline) {
        .p-timeline-event:nth-child(even) {
            flex-direction: row;

            .p-timeline-event-content {
                text-align: left;
            }
        }

        .p-timeline-event-opposite {
            flex: 0;
        }
    }
}
</style>
