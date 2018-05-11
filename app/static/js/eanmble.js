$(document).ready(main);

function main(){
    $('.date-picker').datepicker({
    dateFormat: 'yyyy-mm-dd',
    changeMonth: true,
    changeYear: true
});
}