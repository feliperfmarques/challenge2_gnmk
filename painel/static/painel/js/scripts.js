function panels(source){

  genes = document.getElementsByName('genes');

  for(i = 0; i < genes.length; i++){

        if(source.value.split("_")[1].indexOf(genes[i].value.split("_", 1)) >= 0){

            genes[i].checked = source.checked;

        }
    }
}
