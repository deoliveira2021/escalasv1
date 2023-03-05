const courseNameInput = document.querySelector('#nguerra');
const courseRatingInput = document.querySelector('#escalaSearch');
const addBtn = document.querySelector('#btn-Escala');
const courseList = document.querySelector('#course-list');

addBtn.addEventListener('click', () => {
    const enteredCourseName = courseNameInput.value;
    const enteredCourseRating = courseRatingInput.value;

    if (
        enteredCourseName.trim().length <=0 || 
        enteredCourseRating.trim().length <=0 || 
        enteredCourseRating < 1 || 
        enteredCourseRating > 5
    ) {
        const alert = document.createElement('alert');
        alert.header = 'Entrada Inválida!';
        alert.message = 'Entre com um nome de curso e nota válidos';
        alert.buttons = ['OK'];
        document.body.appendChild(alert);
        return alert.present();
    }

    const newItem = document.createElement('ion-item');
    newItem.innerHTML = `<strong>${enteredCourseName}:</strong> &nbsp;${enteredCourseRating}/5`;

    courseList.appendChild(newItem);

    courseNameInput.value = '';
    courseRatingInput.value = '';
})
