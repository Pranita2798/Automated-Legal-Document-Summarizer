# 🏛️ Automated Legal Document Summarizer

A comprehensive AI-powered tool for analyzing legal documents with advanced text processing capabilities including chunking, summarization, and keyword extraction.

## 🚀 Features

### Core Functionality
- **Text Chunking**: Break down large legal documents into manageable segments
- **AI Summarization**: Generate concise summaries using state-of-the-art language models
- **Keyword Extraction**: Identify important legal terms and phrases
- **Named Entity Recognition**: Extract persons, organizations, and legal entities
- **Interactive Web Interface**: User-friendly Streamlit application

### Advanced Capabilities
- **Multiple Chunking Methods**: Word-based, sentence-based, and paragraph-based chunking
- **Configurable Summarization**: Extractive and abstractive summarization with length control
- **Legal-Specific Processing**: Specialized handling of legal terminology and document structure
- **Batch Processing**: Process multiple documents efficiently
- **Export Options**: Save results in various formats (TXT, JSON)

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Hugging Face Transformers**: State-of-the-art NLP models
- **PyTorch**: Deep learning framework
- **NLTK/SpaCy**: Natural language processing utilities

### Frontend
- **Streamlit**: Interactive web application framework
- **Plotly**: Interactive visualizations
- **Matplotlib/Seaborn**: Statistical plotting
- **WordCloud**: Keyword visualization

### AI Models
- **BART**: Abstractive summarization (facebook/bart-large-cnn)
- **BERT**: Named entity recognition
- **Custom Legal Processing**: Domain-specific optimizations

## 📦 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip package manager
```

### Setup
1. **Clone the repository**
```bash
git clone https://github.com/yourusername/legal-document-summarizer.git
cd legal-document-summarizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download additional models (optional)**
```bash
python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"
```

## 🎯 Usage

### Web Application
Launch the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

Navigate to `http://localhost:8501` in your browser to access the application.

### Command Line Scripts

#### Text Chunking
```bash
python scripts/text_chunking.py input_document.txt --method words --size 200 --overlap 20
```

#### Summarization
```bash
python scripts/summarization.py input_document.txt --type abstractive --length medium
```

#### Keyword Extraction
```bash
python scripts/keyword_extraction.py input_document.txt --min-freq 2 --max-keywords 50
```

### Script Parameters

#### Text Chunking Options
- `--method`: Chunking method (words, sentences, paragraphs)
- `--size`: Number of units per chunk
- `--overlap`: Overlap between consecutive chunks
- `--output`: Output file path

#### Summarization Options
- `--type`: Summarization type (abstractive, extractive)
- `--length`: Summary length (short, medium, long)
- `--model`: Hugging Face model name
- `--output`: Output file path

#### Keyword Extraction Options
- `--min-freq`: Minimum frequency for keyword inclusion
- `--max-keywords`: Maximum number of keywords to extract
- `--model`: NER model name
- `--output`: Output file path

## 📊 Web Interface Guide

### Document Upload
1. Upload a plain text file (.txt) containing your legal document
2. The system will automatically analyze the document structure
3. View document statistics (words, sentences, paragraphs)

### Analysis Options

#### Text Chunking
- Configure chunking method and parameters
- View interactive chunk size distribution
- Download processed chunks

#### Summarization
- Choose between extractive and abstractive summarization
- Adjust summary length and complexity
- View compression statistics

#### Keyword Extraction
- Extract domain-specific legal terms
- Visualize keyword frequency and categories
- Generate word clouds and category distributions

#### Complete Analysis
- Run all analysis types in sequence
- View comprehensive results in tabbed interface
- Export complete analysis report

## 🔧 Configuration

### Model Configuration
The application uses several pre-trained models:

- **Summarization**: `facebook/bart-large-cnn`
- **Named Entity Recognition**: `dbmdz/bert-large-cased-finetuned-conll03-english`
- **Tokenization**: Automatic tokenizer selection

### Legal Domain Customization
The system includes specialized processing for legal documents:

- **Legal terminology recognition**: Contract terms, legal actions, financial terms
- **Document structure analysis**: Clause identification, party recognition
- **Citation processing**: Legal citation normalization
- **Phrase pattern matching**: Common legal phrase extraction

## 📁 Project Structure

```
legal-document-summarizer/
├── scripts/
│   ├── text_chunking.py          # Text chunking functionality
│   ├── summarization.py          # Document summarization
│   └── keyword_extraction.py     # Keyword and phrase extraction
├── streamlit_app.py              # Web application interface
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── examples/
    └── sample_lease_agreement.txt # Sample legal document
```

## 🚀 Performance Optimization

### Hardware Recommendations
- **CPU**: Multi-core processor for parallel processing
- **Memory**: 8GB+ RAM for large documents
- **GPU**: CUDA-compatible GPU for faster AI inference (optional)

### Processing Tips
- **Large Documents**: Use chunking for documents > 10,000 words
- **Batch Processing**: Process multiple documents in sequence
- **Model Caching**: Models are automatically cached after first use

## 📈 Examples

### Sample Output

#### Document Summary
```
LEGAL DOCUMENT SUMMARY
==============================

Original Document: lease_agreement.txt
Summary Type: abstractive
Length: medium
Compression Ratio: 73.2%

SUMMARY:
This lease agreement establishes a one-year rental arrangement between ABC Properties LLC and John Smith for property at 123 Main Street. The tenant agrees to pay $1,200 monthly rent with a $1,200 security deposit. Both parties retain termination rights with 30-day notice.
```

#### Extracted Keywords
```
KEYWORDS:
- agreement (15 occurrences) - contract_terms
- tenant (12 occurrences) - parties
- landlord (10 occurrences) - parties
- property (8 occurrences) - property_terms
- payment (6 occurrences) - financial_terms
```

### Use Cases
- **Contract Review**: Quickly understand key terms and obligations
- **Legal Research**: Extract relevant terms and concepts
- **Document Processing**: Prepare documents for further analysis
- **Client Communication**: Generate summaries for non-legal stakeholders

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Commit changes**: `git commit -m 'Add your feature'`
4. **Push to branch**: `git push origin feature/your-feature`
5. **Submit a pull request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black scripts/ streamlit_app.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- **Multi-format support**: PDF, DOCX, HTML document processing
- **Advanced visualizations**: Interactive document structure mapping
- **API integration**: RESTful API for programmatic access
- **Cloud deployment**: Docker containerization and cloud hosting
- **Collaboration features**: Multi-user document sharing and annotation

## 📞 Support

For questions, issues, or contributions:

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and API reference
- **Community**: Join our discussions and share feedback

## 🙏 Acknowledgments

- **Hugging Face**: For providing state-of-the-art NLP models
- **Streamlit**: For the excellent web application framework
- **Open Source Community**: For the many libraries that make this project possible

---

**Built with ❤️ for the legal technology community**