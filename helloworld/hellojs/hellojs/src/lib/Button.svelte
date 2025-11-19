<script>
	let props=$props();
</script>

	<button 
		{...props}>
		{@render props.children()}
	</button>

<style>
    
    .primary:hover{
        background-color:cornflowerblue;
    }
	.primary{
        color:white;
		background-color:blue;
	}
	.danger {
        color:white;
		background-color:red;
	}
    .danger:hover{
        background-color:orange;
    }
	.sm {
		font-size:1em;
		padding:0.1em;
	}
	.lg {
		font-size:2em
	}
</style>