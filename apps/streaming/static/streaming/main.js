$(document).ready(function(){

    $('#next-song').click(function(e){
        const todaysWord = $('todaysWord').innerHTML;
        console.log("WORD: ", todaysWord);
        $.ajax({
            url: '/new-song',
            word: todaysWord
        }).done(function(res){
            alert(res, typeof res);
        })
    })


})