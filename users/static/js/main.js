const urls = "http://127.0.0.1:8000/api/voter-id/";
const bmaurl = "http://127.0.0.1:8000/api/bma/";

const Get = (yourUrl) =>{
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    //console.log(Httpreq.responseText)
    //console.log(Httpreq.responseText.updateTime)
    return Httpreq.responseText;
}


const data = JSON.parse(Get(urls));
const bmadata = JSON.parse(Get(bmaurl));
console.log(data);
console.log(bmadata);

const submit = document.querySelector('.submit');
const voterid = document.getElementById('id_nid');
const bma = document.getElementById('id_bma');
const institute = document.getElementById('id_institute')
const verified = document.getElementById("id_verified")
// voterid.addEventListener('change', () => {
//     v = voterid.value
//     for(let i=0; i< data.length; i++){
//         if(v === data[i].voter_id){
//             verified.value = 'yes'
//             break;
//         }else{
//             verified.value = 'no'
//         }
//     }
// })
submit.addEventListener('click', () => {
    v = voterid.value
    b = bma.value
    let vrf = 0;
    let brf = 0;
    for(let i=0; i< data.length; i++){
        if(v === data[i].voter_id){
            vrf = 1;
            break;
        }
    }
    for(let i=0; i< bmadata.length; i++){
        if(b === bmadata[i].code){
            brf = 1;
            institute.value = bmadata[i].institute;
            break;
        }
    }
    if(vrf === 1 && brf === 1){
        verified.value = 'yes';
    }else{
        verified.value = 'no';
    }
});
