--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Homebrew)
-- Dumped by pg_dump version 17.2 (Homebrew)

-- Started on 2025-02-05 11:29:34 EST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16848)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3754 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16899)
-- Name: document; Type: TABLE; Schema: public; Owner: affan
--

CREATE TABLE public.document (
    name character varying(255) NOT NULL,
    company character varying(255)
);


ALTER TABLE public.document OWNER TO affan;

--
-- TOC entry 219 (class 1259 OID 16894)
-- Name: tag; Type: TABLE; Schema: public; Owner: affan
--

CREATE TABLE public.tag (
    tag_name character varying(255) NOT NULL
);


ALTER TABLE public.tag OWNER TO affan;

--
-- TOC entry 218 (class 1259 OID 16885)
-- Name: testcase; Type: TABLE; Schema: public; Owner: affan
--

CREATE TABLE public.testcase (
    test_case_id uuid DEFAULT gen_random_uuid() NOT NULL,
    question text NOT NULL,
    ideal_answer text NOT NULL,
    agent_name character varying(255) NOT NULL,
    created_on timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.testcase OWNER TO affan;

--
-- TOC entry 221 (class 1259 OID 16906)
-- Name: testcasehastag; Type: TABLE; Schema: public; Owner: affan
--

CREATE TABLE public.testcasehastag (
    test_case_id uuid NOT NULL,
    tag_name character varying(255) NOT NULL
);


ALTER TABLE public.testcasehastag OWNER TO affan;

--
-- TOC entry 222 (class 1259 OID 16921)
-- Name: testcasereferstodocument; Type: TABLE; Schema: public; Owner: affan
--

CREATE TABLE public.testcasereferstodocument (
    test_case_id uuid NOT NULL,
    document_name character varying(255) NOT NULL,
    pages text NOT NULL
);


ALTER TABLE public.testcasereferstodocument OWNER TO affan;

--
-- TOC entry 3595 (class 2606 OID 16905)
-- Name: document document_pkey; Type: CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (name);


--
-- TOC entry 3593 (class 2606 OID 16898)
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (tag_name);


--
-- TOC entry 3591 (class 2606 OID 16893)
-- Name: testcase testcase_pkey; Type: CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcase
    ADD CONSTRAINT testcase_pkey PRIMARY KEY (test_case_id);


--
-- TOC entry 3597 (class 2606 OID 16910)
-- Name: testcasehastag testcasehastag_pkey; Type: CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcasehastag
    ADD CONSTRAINT testcasehastag_pkey PRIMARY KEY (test_case_id, tag_name);


--
-- TOC entry 3599 (class 2606 OID 16927)
-- Name: testcasereferstodocument testcasereferstodocument_pkey; Type: CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcasereferstodocument
    ADD CONSTRAINT testcasereferstodocument_pkey PRIMARY KEY (test_case_id, document_name);


--
-- TOC entry 3600 (class 2606 OID 16916)
-- Name: testcasehastag testcasehastag_tag_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcasehastag
    ADD CONSTRAINT testcasehastag_tag_name_fkey FOREIGN KEY (tag_name) REFERENCES public.tag(tag_name) ON DELETE CASCADE;


--
-- TOC entry 3601 (class 2606 OID 16911)
-- Name: testcasehastag testcasehastag_test_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcasehastag
    ADD CONSTRAINT testcasehastag_test_case_id_fkey FOREIGN KEY (test_case_id) REFERENCES public.testcase(test_case_id) ON DELETE CASCADE;


--
-- TOC entry 3602 (class 2606 OID 16933)
-- Name: testcasereferstodocument testcasereferstodocument_document_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcasereferstodocument
    ADD CONSTRAINT testcasereferstodocument_document_name_fkey FOREIGN KEY (document_name) REFERENCES public.document(name) ON DELETE CASCADE;


--
-- TOC entry 3603 (class 2606 OID 16928)
-- Name: testcasereferstodocument testcasereferstodocument_test_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: affan
--

ALTER TABLE ONLY public.testcasereferstodocument
    ADD CONSTRAINT testcasereferstodocument_test_case_id_fkey FOREIGN KEY (test_case_id) REFERENCES public.testcase(test_case_id) ON DELETE CASCADE;


-- Completed on 2025-02-05 11:29:35 EST

--
-- PostgreSQL database dump complete
--

