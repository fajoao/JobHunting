// React runtime for the dashboard, loaded before app.js (which reads these globals).
import * as React from 'react'
import * as ReactDOM from 'react-dom'
import * as ReactDOMClient from 'react-dom/client'
import * as ReactJSX from 'react/jsx-runtime'

Object.assign(window, { React, ReactDOM, ReactDOMClient, ReactJSX })
