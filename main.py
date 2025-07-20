import streamlit as st
from config import setup_language, get_translation
from data_models import DataModel, get_available_models
from generator import generate_data
from exporter import export_data
import utils
import os

# إعداد الصفحة
st.set_page_config(
    page_title="Data Generator Pro",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل الترجمة
current_language = setup_language()
_ = get_translation(current_language)

# شريط التنقل العلوي
st.markdown(utils.load_css(), unsafe_allow_html=True)

# القائمة الرئيسية
menu_options = {
    "home": _("Home"),
    "generate": _("Generate Data"),
    "export": _("Export Data"),
    "connect": _("Connect to BI Tools"),
    "settings": _("Settings")
}

with st.sidebar:
    st.image("assets/logo.png", width=150)
    selected_menu = st.radio(
        _("Main Menu"),
        list(menu_options.keys()),
        format_func=lambda x: menu_options[x]
    )

# الصفحة الرئيسية
if selected_menu == "home":
    st.title(_("Professional Data Generator"))
    st.markdown(_("""
    ## Welcome to Data Generator Pro
    
    This powerful tool allows you to:
    - Generate millions of rows of realistic data
    - Customize data types and patterns
    - Export to multiple formats
    - Connect with BI tools like Tableau and Power BI
    """))

# صفحة توليد البيانات
elif selected_menu == "generate":
    st.title(_("Data Generation"))
    
    # البحث عن نموذج البيانات
    search_term = st.text_input(_("Search for data model..."))
    available_models = get_available_models(search_term)
    
    if available_models:
        selected_model = st.selectbox(
            _("Select Data Model"),
            available_models,
            format_func=lambda x: x.name
        )
        
        # عرض تفاصيل النموذج
        if selected_model:
            with st.expander(_("Model Details")):
                st.write(selected_model.description)
                st.json(selected_model.schema)
            
            # تخصيص النموذج
            with st.expander(_("Customize Fields")):
                customized_fields = []
                for field in selected_model.fields:
                    col1, col2 = st.columns(2)
                    with col1:
                        enabled = st.checkbox(
                            f"Enable {field.name}",
                            value=True,
                            key=f"enable_{field.name}"
                        )
                    with col2:
                        if enabled:
                            field_type = st.selectbox(
                                f"Type for {field.name}",
                                field.available_types,
                                index=field.available_types.index(field.type),
                                key=f"type_{field.name}"
                            )
                            customized_fields.append(field.copy(update={"type": field_type}))
            
            # إعدادات التوليد
            with st.expander(_("Generation Settings")):
                rows = st.number_input(_("Number of Rows"), 1, 10000000, 1000)
                batch_size = st.number_input(_("Batch Size"), 1, 100000, 1000)
                seed = st.number_input(_("Random Seed"), value=42)
            
            # توليد البيانات
            if st.button(_("Generate Data")):
                with st.spinner(_("Generating data...")):
                    data = generate_data(
                        model=selected_model.copy(update={"fields": customized_fields}),
                        rows=rows,
                        batch_size=batch_size,
                        seed=seed
                    )
                    st.session_state.generated_data = data
                    st.success(_(f"Successfully generated {rows} rows of data!"))
                    st.dataframe(data.head(50))

# صفحة التصدير
elif selected_menu == "export":
    st.title(_("Export Data"))
    
    if "generated_data" not in st.session_state:
        st.warning(_("No data to export. Please generate data first."))
    else:
        data = st.session_state.generated_data
        
        # خيارات التصدير
        export_format = st.selectbox(
            _("Export Format"),
            ["CSV", "Excel", "JSON", "Parquet", "SQL", "Cloud Storage"]
        )
        
        if export_format in ["CSV", "Excel", "JSON", "Parquet"]:
            file_name = st.text_input(_("File Name"), "generated_data")
            if st.button(_("Export")):
                output = export_data(data, export_format.lower(), file_name)
                st.success(_(f"Data exported successfully to {output}"))
                with open(output, "rb") as f:
                    st.download_button(
                        label=_("Download File"),
                        data=f,
                        file_name=os.path.basename(output)
                    )
        
        elif export_format == "SQL":
            db_type = st.selectbox(_("Database Type"), ["MySQL", "PostgreSQL", "SQLite"])
            connection_string = st.text_input(_("Connection String"))
            table_name = st.text_input(_("Table Name"), "generated_data")
            if st.button(_("Export to Database")):
                with st.spinner(_("Exporting to database...")):
                    export_data(data, "sql", table_name, db_type, connection_string)
                    st.success(_("Data exported to database successfully!"))
        
        elif export_format == "Cloud Storage":
            cloud_provider = st.selectbox(_("Cloud Provider"), ["AWS S3", "Google Cloud Storage", "Azure Blob"])
            bucket_name = st.text_input(_("Bucket Name"))
            file_path = st.text_input(_("File Path"), "generated_data.parquet")
            if st.button(_("Upload to Cloud")):
                with st.spinner(_("Uploading to cloud storage...")):
                    export_data(data, "cloud", file_path, cloud_provider, bucket_name)
                    st.success(_("Data uploaded to cloud storage successfully!"))

# صفحة الاتصال بأدوات BI
elif selected_menu == "connect":
    st.title(_("Connect to BI Tools"))
    
    bi_tool = st.selectbox(
        _("Select BI Tool"),
        ["Tableau", "Power BI", "Looker", "Metabase"]
    )
    
    if bi_tool == "Tableau":
        st.markdown(_("""
        ### Tableau Integration
        1. For live connection, use the database export option
        2. For extracted data, download as CSV/Excel and connect
        3. For large datasets, use the cloud storage option
        """))
    
    elif bi_tool == "Power BI":
        st.markdown(_("""
        ### Power BI Integration
        1. Use 'Get Data' and select the appropriate source
        2. For cloud storage, use the respective connector
        3. For databases, use the SQL connection
        """))
    
    st.info(_("For advanced integration, please contact support."))

# صفحة الإعدادات
elif selected_menu == "settings":
    st.title(_("Settings"))
    
    # إعدادات اللغة
    new_language = st.selectbox(
        _("Language"),
        ["English", "العربية"],
        index=0 if current_language == "en" else 1
    )
    
    if st.button(_("Save Settings")):
        st.session_state.language = "en" if new_language == "English" else "ar"
        st.experimental_rerun()
    
    # إعدادات الأداء
    st.subheader(_("Performance Settings"))
    cache_size = st.slider(_("Cache Size (MB)"), 10, 1000, 100)
    max_threads = st.slider(_("Max Threads"), 1, 16, 4)
    
    # معلومات النظام
    st.subheader(_("System Information"))
    st.text(_(f"Streamlit version: {st.__version__}"))
    st.text(_(f"Python version: {utils.get_python_version()}"))
    st.text(_(f"OS: {utils.get_os_info()}"))
