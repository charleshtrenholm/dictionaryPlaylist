$(document).ready(function(){

    $('#next-song').click(function(e){
        console.log('its working')
        const todaysWord = $('#todaysWord').text();
        console.log("WORD: ", todaysWord);
        $.ajax({
            url: '/new-song',
            data: {
                'word': todaysWord
            }
        }).done(function(res){
            alert(res, typeof res);
        })
    })


})