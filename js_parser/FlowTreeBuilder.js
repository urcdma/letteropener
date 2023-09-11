const traverse = require('@babel/traverse');
const { DefinitionsList } = require('./entryDefinitionsMap');
const { parseCodeToAST, buildVisitor } = require('./astBuilder');
const { ABSTRACTION_LEVELS, rebuildConfigForAbstractionLevel } = require('./abstractionLevelsConfigurator');
const FlowTreeModifier = require('./FlowTreeModifier');
const {
    DEFINED_MODIFIERS,
    MODIFIER_PRESETS,
    destructionModifier,
    expressionCallbacksModifier,
    arrowFunctionReturnModifier
} = require('./modifiers/modifiersFactory');
const { TOKEN_TYPES } = require('shared/constants');
const { logError } = require('shared/utils/logger');

const buildFlowTree = (astTree, astVisitorConfig) => {
    const treeNodes = [];

    traverse(astTree, buildVisitor(astVisitorConfig, treeNodes));

    const root = (treeNodes.length && treeNodes[0]) || {};
    return root.type === TOKEN_TYPES.PROGRAM
        ? root
        : { name: 'Root', type: TOKEN_TYPES.PROGRAM, body: treeNodes };
};

const createFlowTreeModifier = () => {
    const modifiers = FlowTreeModifier();

    return {
        setModifier(modifier) {
            modifiers.addModifier(modifier);
        },

        registerNewModifier(test, updates) {
            modifiers.create(test, updates);
        },

        destructNodeTree(test, newNameFn) {
            this.setModifier(destructionModifier(test, newNameFn));
        },

        applyToFlowTree(flowTree) {
            modifiers.applyTo(flowTree);
            return flowTree;
        }
    };
};

const flowTreeBuilder = ({ astParser = {}, astVisitor = {} } = {}) => {
    const astParserConfig = {
        ...astParser
    };

    const astVisitorConfig = {
        definitionsMap: [...DefinitionsList],
        globalIgnore: null,
        ...astVisitor
    };

    const defaultModifier = createFlowTreeModifier();
    defaultModifier.setModifier(expressionCallbacksModifier());
    defaultModifier.setModifier(arrowFunctionReturnModifier());

    return {
        setAbstractionLevel(level) {
            astVisitorConfig.definitionsMap = rebuildConfigForAbstractionLevel(level);
        },

        resetAbstractionLevelToNormal() {
            astVisitorConfig.definitionsMap = [...DefinitionsList];
        },

        setIgnoreFilter(fn) {
            astVisitorConfig.globalIgnore = fn;
        },

        build(code) {
            const ast = this.buildAst(code);
            return this.buildFlowTreeFromAst(ast);
        },

        buildAst(code) {
            return parseCodeToAST(code, astParserConfig);
        },

        buildFlowTreeFromAst(ast) {
            let flowTree = [];

            try {
                flowTree = buildFlowTree(ast, astVisitorConfig);
                defaultModifier.applyToFlowTree(flowTree);
            } catch (e) {
                logError('Error at buildFlowTreeFromAst' + e.message, e.stack);
                throw e;
            }

            return flowTree;
        }
    };
};

module.exports = {
    flowTreeBuilder,
    DEFINED_MODIFIERS,
    MODIFIER_PRESETS,
    ABSTRACTION_LEVELS,
    createFlowTreeModifier
};
