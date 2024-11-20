import streamlit as st
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from injector import get_admin_repository


class SectorManagementUI:
    def __init__(self):
        self.admin_repository = get_admin_repository()
        self._initialize_session_state()

    def _initialize_session_state(self):
        state_keys = [
            "edit_sector",
            "delete_sector",
            "error_message",
            "success_message",
        ]

        for key in state_keys:
            if key not in st.session_state:
                st.session_state[key] = None

    def _clear_messages(self):
        st.session_state.error_message = None
        st.session_state.success_message = None

    def _display_messages(self):
        if st.session_state.error_message:
            st.error(st.session_state.error_message)
        if st.session_state.success_message:
            st.success(st.session_state.success_message)

    def _add_sector_form(self):
        with st.form("Add Sector", clear_on_submit=True):
            name = st.text_input("Sector Name")
            submitted = st.form_submit_button("Add Sector")

            if submitted:
                self._clear_messages()
                try:
                    self.admin_repository.create_sector(name.strip())
                    st.session_state.success_message = "Sector added successfully!"
                    st.rerun()
                except Exception as e:
                    self._handle_exception("adding", e)

    def _render_sector_list(self):
        try:
            sectors = self.admin_repository.list_sectors()

            if not sectors:
                st.info("No sectors found. Add a sector to get started.")
                return

            for sector in sectors:
                safe_sector_key = "".join(e if e.isalnum() else "_" for e in sector)

                col1, col2, col3 = st.columns([0.8, 0.8, 8.6])

                with col1:
                    edit_button = st.button(
                        "✏️",
                        key=f"edit_{safe_sector_key}",
                        help="Edit",
                    )
                with col2:
                    delete_button = st.button(
                        "🗑️",
                        key=f"delete_{safe_sector_key}",
                        help="Delete",
                    )
                with col3:
                    st.write(sector)

                if edit_button:
                    st.session_state.edit_sector = sector
                    st.session_state.delete_sector = None
                    st.rerun()
                if delete_button:
                    st.session_state.delete_sector = sector
                    st.session_state.edit_sector = None
                    st.rerun()

                if st.session_state.edit_sector == sector:
                    self._edit_sector_form(sector)

                elif st.session_state.delete_sector == sector:
                    self._delete_sector_confirmation(sector)

        except SQLAlchemyError as e:
            st.error(f"Error retrieving sectors: {str(e)}")

    def _edit_sector_form(self, sector):
        self._clear_messages()
        with st.container(border=True):
            new_name = st.text_input("New Name", value=sector, key=f"new_name_{sector}")
            col1, col2 = st.columns([1, 7])
            with col1:
                update_button = st.button("Update", key=f"update_{sector}")
            with col2:
                cancel_button = st.button("Cancel", key=f"cancel_{sector}")

        if update_button:
            try:
                self.admin_repository.update_sector(
                    old_name=sector, new_name=new_name.strip()
                )
                st.session_state.success_message = "Sector renamed successfully."
                st.session_state.edit_sector = None
                st.rerun()
            except Exception as e:
                self._handle_exception("editing", e)

        if cancel_button:
            st.session_state.edit_sector = None
            st.rerun()

    def _delete_sector_confirmation(self, sector):
        self._clear_messages()
        with st.container(border=True):
            st.warning(f"Are you sure you want to delete '{sector}'?")
            col1, col2 = st.columns([1, 11])
            with col1:
                confirm_button = st.button("Yes", key=f"confirm_delete_{sector}")
            with col2:
                cancel_button = st.button("No", key=f"cancel_delete_{sector}")

        if confirm_button:
            try:
                self.admin_repository.delete_sector(sector)
                st.session_state.success_message = f"Sector '{sector}' deleted."
                st.session_state.delete_sector = None
                st.rerun()
            except Exception as e:
                self._handle_exception("deleting", e)

        if cancel_button:
            st.session_state.delete_sector = None
            st.rerun()

    def _handle_exception(self, action, e):
        if isinstance(e, IntegrityError):
            st.session_state.error_message = "Sector with this name already exists."
        else:
            st.session_state.error_message = f"Error {action} sector: {str(e)}"
        st.rerun()

    def render(self):
        st.title("MoneyMonkey: Sector Management")

        tabs = st.tabs(["Sectors", "Industries", "Data Sources"])

        with tabs[0]:
            self._add_sector_form()
            self._display_messages()
            st.subheader("List of Sectors")
            self._render_sector_list()

    def run(self):
        self.render()


def main():
    ui = SectorManagementUI()
    ui.run()


if __name__ == "__main__":
    main()
