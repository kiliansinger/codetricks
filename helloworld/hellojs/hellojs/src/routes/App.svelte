<script>
    
	import Button from '$lib/Button.svelte';

    let props = $props();
    
    let num = $state("");
    
    import { onMount } from 'svelte';

    async function doFetch() {
            const url = "/api/random";
            try {
                const response = await fetch(url+"?"+new URLSearchParams({
                    from: 10,
                    to: 20,
                }).toString());
                if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
                }

                const json = await response.json();
                console.log(json);
                num=json.number;
            } catch (error) {
                console.error(error.message);
            }
        }

	onMount(doFetch);

</script>


<Button class="primary sm" onclick={async()=>doFetch()}>
	Update
</Button>

<Button class="danger lg" onclick={()=>console.log("Clicked")}>
	Click
</Button>
<h1>Hello, {props.name} {num}!</h1>