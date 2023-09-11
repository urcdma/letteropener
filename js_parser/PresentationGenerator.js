const { parseCodeToAST } = require('builder/astBuilder');
const FlowTreeBuilder = require('builder/FlowTreeBuilder').default;
const {
    ABSTRACTION_LEVELS,
    MODIFIER_PRESETS,
    DEFINED_MODIFIERS
} = require('builder/FlowTreeBuilder');
const SVGRender = require('render/svg/SVGRender').default;
const { TOKEN_TYPES, MODIFIED_TYPES } = require('shared/constants');

const buildTreeByAbstractionLevels = levels => {
    const flowTreeBuilder = FlowTreeBuilder();
    flowTreeBuilder.setAbstractionLevel(levels);

    return astTree => flowTreeBuilder.buildFlowTreeFromAst(astTree);
};

const generateExportSlideTree = buildTreeByAbstractionLevels(ABSTRACTION_LEVELS.EXPORT);

const generateImportExportSlideTree = buildTreeByAbstractionLevels([
    ABSTRACTION_LEVELS.EXPORT,
    ABSTRACTION_LEVELS.IMPORT
]);

const generateClassFunctionSlideTree = buildTreeByAbstractionLevels([
    ABSTRACTION_LEVELS.EXPORT,
    ABSTRACTION_LEVELS.IMPORT,
    ABSTRACTION_LEVELS.CLASS,
    ABSTRACTION_LEVELS.FUNCTION
]);

const generateClassFunctionDependenciesSlideTree = buildTreeByAbstractionLevels([
    ABSTRACTION_LEVELS.EXPORT,
    ABSTRACTION_LEVELS.IMPORT,
    ABSTRACTION_LEVELS.CLASS,
    ABSTRACTION_LEVELS.FUNCTION,
    ABSTRACTION_LEVELS.FUNCTION_DEPENDENCIES
]);

const generateRegularSlideTree = astTree => {
    const flowTreeBuilder = FlowTreeBuilder();
    return flowTreeBuilder.buildFlowTreeFromAst(astTree);
};

const buildSlides = code => {
    const svgRender = SVGRender(),
        astTree = parseCodeToAST(code);

    const slides = [
        generateExportSlideTree(astTree),
        generateImportExportSlideTree(astTree),
        generateClassFunctionSlideTree(astTree),
        generateClassFunctionDependenciesSlideTree(astTree),
        generateRegularSlideTree(astTree)
    ];

    return slides
        .filter(slide => slide.body.length)
        .map(svgRender.buildShapesTree)
        .map(shapesTree => shapesTree.print());
};

module.exports = {
    buildSlides,
    generateExportSlideTree,
    generateImportExportSlideTree,
    generateClassFunctionSlideTree,
    generateClassFunctionDependenciesSlideTree,
    generateRegularSlideTree
};
