import streamlit as st
from config import setup_language, get_translation
from data_models import DataModel, get_available_models
from generator import generate_data
from exporter import export_data
import utils
import os
import time

# إعداد الصفحة
st.set_page_config(
    page_title="Data Generator Pro",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل الترجمة
current_language = setup_language()

# شريط التنقل العلوي
st.markdown(utils.load_css(), unsafe_allow_html=True)

# القائمة الرئيسية
menu_options = {
    "home": get_translation(current_language, "Home"),
    "generate": get_translation(current_language, "Generate Data"),
    "export": get_translation(current_language, "Export Data"),
    "connect": get_translation(current_language, "Connect to BI Tools"),
    "settings": get_translation(current_language, "Settings")
}

with st.sidebar:
    st.image("assets/logo.png", width=150)
    selected_menu = st.radio(
        get_translation(current_language, "Main Menu"),
        list(menu_options.keys()),
        format_func=lambda x: menu_options[x]
    )

# الصفحة الرئيسية
if selected_menu == "home":
    st.title(get_translation(current_language, "Professional Data Generator"))
    st.markdown(get_translation(current_language, """
    ## Welcome to Data Generator Pro
    
    This powerful tool allows you to:
    - Generate millions of rows of realistic data
    - Customize data types and patterns
    - Export to multiple formats
    - Connect with BI tools like Tableau and Power BI
    """))

# صفحة توليد البيانات
elif selected_menu == "generate":
    st.title(get_translation(current_language, "Data Generation"))
    
    # البحث عن نموذج البيانات مع مؤشر تحميل
    search_term = st.text_input(get_translation(current_language, "Search for data model..."))
    
    start_time = time.time()
    with st.spinner(get_translation(current_language, "Loading models...")):
        available_models = get_available_models(search_term)
        load_time = time.time() - start_time
    
    st.caption(f"Loaded {len(available_models)} models in {load_time:.2f} seconds")
    
    if available_models:
        selected_model = st.selectbox(
            get_translation(current_language, "Select Data Model"),
            available_models,
            format_func=lambda x: x.name
        )
        
        # عرض تفاصيل النموذج
        if selected_model:
            with st.expander(get_translation(current_language, "Model Details")):
                st.write(selected_model.description)
                st.json(selected_model.schema)
            
            # تخصيص النموذج
            with st.expander(get_translation(current_language, "Customize Fields")):
                customized_fields = []
                for field in selected_model.fields:
                    col1, col2 = st.columns(2)
                    with col1:
                        enabled = st.checkbox(
                            f"{get_translation(current_language, 'Enable')} {field.name}",
                            value=True,
                            key=f"enable_{field.name}"
                        )
                    with col2:
                        if enabled:
                            field_type = st.selectbox(
                                f"{get_translation(current_language, 'Type for')} {field.name}",
                                field.available_types,
                                index=field.available_types.index(field.type),
                                key=f"type_{field.name}"
                            )
                            customized_fields.append(field.copy(update={"type": field_type}))
            
            # إعدادات التوليد
            with st.expander(get_translation(current_language, "Generation Settings")):
                rows = st.number_input(get_translation(current_language, "Number of Rows"), 1, 10000000, 1000)
                batch_size = st.number_input(get_translation(current_language, "Batch Size"), 1, 100000, 1000)
                seed = st.number_input(get_translation(current_language, "Random Seed"), value=42)
            
            # توليد البيانات
            if st.button(get_translation(current_language, "Generate Data")):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                start_time = time.time()
                with st.spinner(get_translation(current_language, "Generating data...")):
                    data = generate_data(
                        model=selected_model.copy(update={"fields": customized_fields}),
                        rows=rows,
                        batch_size=batch_size,
                        seed=seed,
                        progress_callback=lambda p: (progress_bar.progress(p), 
                                                  status_text.text(f"Progress: {p*100:.1f}%"))
                    
                    gen_time = time.time() - start_time
                    st.session_state.generated_data = data
                    st.success(get_translation(current_language, 
                        f"Successfully generated {rows:,} rows in {gen_time:.2f} seconds!"))
                    st.dataframe(data.head(50))



# صفحة التصدير
elif selected_menu == "export":
    st.title(get_translation(current_language, "Export Data"))
    
    if "generated_data" not in st.session_state:
        st.warning(get_translation(current_language, "No data to export. Please generate data first."))
    else:
        data = st.session_state.generated_data
        
        # خيارات التصدير
        export_format = st.selectbox(
            get_translation(current_language, "Export Format"),
            ["CSV", "Excel", "JSON", "Parquet", "SQL", "Cloud Storage"]
        )
        
        if export_format in ["CSV", "Excel", "JSON", "Parquet"]:
            file_name = st.text_input(get_translation(current_language, "File Name"), "generated_data")
            if st.button(get_translation(current_language, "Export")):
                output = export_data(data, export_format.lower(), file_name)
                st.success(get_translation(current_language, f"Data exported successfully to {output}"))
                with open(output, "rb") as f:
                    st.download_button(
                        label=get_translation(current_language, "Download File"),
                        data=f,
                        file_name=os.path.basename(output)
                    )
        
        elif export_format == "SQL":
            db_type = st.selectbox(get_translation(current_language, "Database Type"), ["MySQL", "PostgreSQL", "SQLite"])
            connection_string = st.text_input(get_translation(current_language, "Connection String"))
            table_name = st.text_input(get_translation(current_language, "Table Name"), "generated_data")
            if st.button(get_translation(current_language, "Export to Database")):
                with st.spinner(get_translation(current_language, "Exporting to database...")):
                    export_data(data, "sql", table_name, db_type, connection_string)
                    st.success(get_translation(current_language, "Data exported to database successfully!"))
        
        elif export_format == "Cloud Storage":
            cloud_provider = st.selectbox(get_translation(current_language, "Cloud Provider"), ["AWS S3", "Google Cloud Storage", "Azure Blob"])
            bucket_name = st.text_input(get_translation(current_language, "Bucket Name"))
            file_path = st.text_input(get_translation(current_language, "File Path"), "generated_data.parquet")
            if st.button(get_translation(current_language, "Upload to Cloud")):
                with st.spinner(get_translation(current_language, "Uploading to cloud storage...")):
                    export_data(data, "cloud", file_path, cloud_provider, bucket_name)
                    st.success(get_translation(current_language, "Data uploaded to cloud storage successfully!"))

# صفحة الاتصال بأدوات BI
elif selected_menu == "connect":
    st.title(get_translation(current_language, "Connect to BI Tools"))
    
    bi_tool = st.selectbox(
        get_translation(current_language, "Select BI Tool"),
        ["Tableau", "Power BI", "Looker", "Metabase"]
    )
    
    if bi_tool == "Tableau":
        st.markdown(get_translation(current_language, """
        ### Tableau Integration
        1. For live connection, use the database export option
        2. For extracted data, download as CSV/Excel and connect
        3. For large datasets, use the cloud storage option
        """))
    
    elif bi_tool == "Power BI":
        st.markdown(get_translation(current_language, """
        ### Power BI Integration
        1. Use 'Get Data' and select the appropriate source
        2. For cloud storage, use the respective connector
        3. For databases, use the SQL connection
        """))
    
    st.info(get_translation(current_language, "For advanced integration, please contact support."))

# صفحة الإعدادات
elif selected_menu == "settings":
    st.title(get_translation(current_language, "Settings"))
    
    # إعدادات اللغة
    new_language = st.selectbox(
        get_translation(current_language, "Language"),
        ["English", "العربية"],
        index=0 if current_language == "en" else 1
    )
    
    if st.button(get_translation(current_language, "Save Settings")):
        st.session_state.language = "en" if new_language == "English" else "ar"
     
        st.experimental_rerun()
    
    # إعدادات الأداء
    st.subheader(get_translation(current_language, "Performance Settings"))
    cache_size = st.slider(get_translation(current_language, "Cache Size (MB)"), 10, 1000, 100)
    max_threads = st.slider(get_translation(current_language, "Max Threads"), 1, 16, 4)
    
    # معلومات النظام
    st.subheader(get_translation(current_language, "System Information"))
    st.text(get_translation(current_language, f"Streamlit version: {st.__version__}"))
    st.text(get_translation(current_language, f"Python version: {utils.get_python_version()}"))
    st.text(get_translation(current_language, f"OS: {utils.get_os_info()}"))
