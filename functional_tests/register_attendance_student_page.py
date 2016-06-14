from page_objects import PageObject, PageElement, MultiPageElement


class RegisterStudentPage(PageObject):
    checkboxes = MultiPageElement(xpath="//input[@type='checkbox']")
    submit_button = PageElement(css="input[type='submit']")

    def register(self, student):
        # this is tied to structure of checkboxes generated by django
        # <label for="id_students_0">
        #   <input id="id_students_0" name="students" value="1" type="checkbox"> john
        # </label>
        student_chekboxes = [checkbox for checkbox in self.checkboxes if checkbox.find_element_by_xpath("..").text == student]
        assert len(student_chekboxes) > 0, "student not found in checkboxes"
        student_chekbox = student_chekboxes[0]
        student_chekbox.click()
        self.submit_button.click()
